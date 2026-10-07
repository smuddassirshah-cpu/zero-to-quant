// Spike S1 probe, module 'platform': the platform checks of docs/PLAN.md stage 2 item (c), the single list
// (docs/ARCHITECTURE.md 13 E0 and 14 mirror it).
//
// Decision notes:
// - Every verdict comes from a value the check measured in this frame; anything it cannot measure reads as
//   inconclusive. Raw values go in `data`, conclusions only in `summary`.
// - Nothing personal is recorded: no file names or contents, no full page URL (it may carry the artifact's
//   ids), and a hash that is not one of ours is recorded by its length only.
// - Compression trusts Resource Timing only when its decoded size equals the body this check read, so an
//   entry for another response cannot pass it. Zero sizes fall back to the Content-Encoding header, which
//   is a direct reading of the response; neither gives inconclusive. A missing header counts as "not
//   compressed" only on a same-origin (basic) response: on a cors response the header is not exposed, so
//   equal sizes there give inconclusive, and so does a transferSize that says compressed.
// - document.fonts.check() is true when no face matches at all, so the font check passes only on faces that
//   document.fonts.load() returned with status 'loaded'.
// - The Web Locks bar includes `steal: true`, which the "Use here" button of ARCHITECTURE.md 4.7 needs, and
//   one cross-agent step (a lock held by a dedicated worker), since decision 26 needs the lock manager
//   shared across agents. The lock names carry a per-run suffix so another open probe tab cannot hold them.
// - The hash-route bar includes hashchange firing: the hash router of ARCHITECTURE.md decision 19 needs both.
//   The check walks back over the entries it added, so a later back step does not land on its hashes.
// - The IndexedDB worker check re-derives its verdict from the worker's raw counts. If the module worker does
//   not start, a classic worker runs the same file for comparison; the verdict stays a fail.
// - version.json after the republish is fetched with a fresh query string twice (default cache, then
//   no-store). The fresh query means the browser cache can never answer either fetch, and no-store sends
//   Cache-Control: no-cache upstream, so a v1/v2 split means a cache between the page and the host (or a
//   change between the two fetches). A v1/v1 pair is read again 15 s and 40 s after the signal, since a
//   publish still going live looks the same, and then data/v2-only.json tells a cached version.json from a
//   page scoped to its own version's files. A signal the owner started by hand cannot prove v2 was live,
//   so readings that never change after it give inconclusive.
// - Reload and back-gesture state crosses a reload through ctx.session. The reload marker is also written
//   into the URL hash, since location.reload() keeps the frame's URL and sessionStorage may not survive; it
//   carries a hash of the page's base path (never the path), so a different base path after the reload
//   shows that versions are scoped by URL.
// - The clipboard check keeps only whether the pasted text equals the fixed link and its length, never the
//   text: a clipboard can hold anything.

const N_RECORDS = 100;
const FETCH_TIMEOUT_MS = 10_000;
const RELOAD_KEY = 's1.platform.reload';
const BACK_KEY = 's1.platform.back';
const BACK_RELOADED_KEY = 's1.platform.back.reloaded';
const BACK_PRE = ['Start the swipe test', 'I know already: the swipe closes or leaves the probe'];
const BACK_AFTER_RELOAD = ['It closed or left the probe', 'It reloaded the probe in place', 'Try the swipe again'];
const RE_READ_AT_MS = [15_000, 40_000];
const CLIP_LINK = 'https://claude.ai/s1-clipboard-probe';
const RELOAD_HASH = /^#s1-reload-(v1|v2|unknown)$/;
const SLASH_ROUTE = '#/learn/crs.numwork';
const PLAIN_ANCHOR = '#s1-plain';
const OUR_HASH = /^#(s1-[a-z0-9-]{1,40}|\/learn\/crs\.numwork)$/;
const CODINGS = /\b(gzip|x-gzip|br|deflate|zstd|compress)\b/i;
const HEADERS = ['content-encoding', 'content-length', 'content-type', 'cache-control', 'age', 'etag', 'last-modified', 'vary', 'server', 'cf-cache-status'];
const EXTERNAL_URL = 'https://www.example.org/';
const OPEN_URL = 'https://www.example.org/?s1';
const LINK_CHOICES = ['It opened in a browser', 'It opened inside the Claude app', 'Nothing happened'];
const OPEN_CHOICES = ['A browser or a new view opened', 'It opened inside the Claude app', 'Nothing happened'];
const BACK_CHOICES = ['The probe stayed and went back one step', 'The probe closed or left the artifact', 'Nothing happened'];
const suffix = Math.random().toString(36).slice(2, 8);

// ---- helpers

const r1 = v => Math.round(v * 10) / 10;
const kb = b => `${(b / 1024).toFixed(1)} KB`;
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
const errText = e => {
  if (e == null) return String(e);
  const s = typeof e === 'object' && 'message' in e ? `${e.name || 'Error'}: ${e.message}` : String(e);
  return s.slice(0, 300);
};
const clip = (s, n) => (s.length > n ? `${s.slice(0, n)}... [${s.length - n} more characters]` : s);
const hashLabel = h => (h === '' ? '(none)' : OUR_HASH.test(h) ? h : `other (${h.length} characters)`);
const hashOf = url => {
  try {
    return hashLabel(new URL(url).hash);
  } catch (e) {
    return `unreadable (${errText(e)})`;
  }
};

// Resolves { state: 'resolved', value } | { state: 'rejected', error } | { state: 'timeout' }; never rejects.
function settle(promise, ms) {
  return new Promise(resolve => {
    const timer = setTimeout(() => resolve({ state: 'timeout' }), ms);
    Promise.resolve(promise).then(
      value => { clearTimeout(timer); resolve({ state: 'resolved', value }); },
      error => { clearTimeout(timer); resolve({ state: 'rejected', error }); },
    );
  });
}

function el(tag, props = {}, ...kids) {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(props)) {
    if (v == null || v === false) continue;
    if (k === 'class') n.className = v;
    else if (k === 'text') n.textContent = v;
    else n.setAttribute(k, v === true ? '' : String(v));
  }
  for (const kid of kids) if (kid != null) n.append(kid);
  return n;
}

// Collects events of one type; until(pred, ms) resolves the first item matching pred, or null after ms.
function collector(target, type, map) {
  const items = [];
  let waiters = [];
  const on = e => {
    const v = map(e);
    items.push(v);
    waiters = waiters.filter(w => !w(v));
  };
  target.addEventListener(type, on);
  return {
    items,
    until(pred, ms) {
      const hit = items.find(pred);
      if (hit) return Promise.resolve(hit);
      return new Promise(resolve => {
        const check = v => {
          if (!pred(v)) return false;
          clearTimeout(timer);
          resolve(v);
          return true;
        };
        const timer = setTimeout(() => {
          waiters = waiters.filter(w => w !== check);
          resolve(null);
        }, ms);
        waiters.push(check);
      });
    },
    stop: () => target.removeEventListener(type, on),
  };
}

function pickHeaders(h) {
  const out = {};
  for (const name of HEADERS) {
    const v = h.get(name);
    if (v != null) out[name] = clip(v, 120);
  }
  return out;
}

// One fetch of our own file with a timeout; never rejects. `buffer: true` reads bytes instead of text.
async function getFile(path, init = {}, { buffer = false } = {}) {
  const ac = new AbortController();
  const timer = setTimeout(() => ac.abort(), FETCH_TIMEOUT_MS);
  const t0 = performance.now();
  try {
    const res = await fetch(path, { ...init, signal: ac.signal });
    const body = buffer ? await res.arrayBuffer() : await res.text();
    return { ok: res.ok, status: res.status, type: res.type, redirected: res.redirected, ms: r1(performance.now() - t0), headers: pickHeaders(res.headers), body };
  } catch (e) {
    return { ok: false, status: null, ms: r1(performance.now() - t0), error: ac.signal.aborted ? `no response in ${FETCH_TIMEOUT_MS / 1000} s` : errText(e) };
  } finally {
    clearTimeout(timer);
  }
}

// The version a JSON body names, or null; `text` is kept short for the record.
function versionOf(r) {
  if (!r.ok || typeof r.body !== 'string') return { version: null, text: r.body == null ? null : clip(String(r.body), 120) };
  try {
    const j = JSON.parse(r.body);
    return { version: typeof j?.version === 'string' ? j.version : null, text: clip(r.body.trim(), 200) };
  } catch (e) {
    return { version: null, text: clip(r.body, 120), parseError: errText(e) };
  }
}

const fileRecord = r => {
  const v = versionOf(r);
  return { status: r.status, ok: r.ok, ms: r.ms, version: v.version, body: v.text, ...(v.parseError ? { parseError: v.parseError } : {}), ...(r.error ? { error: r.error } : {}), ...(r.headers ? { headers: r.headers } : {}) };
};

function replaceHash(h) {
  const u = new URL(location.href);
  u.hash = h;
  history.replaceState(history.state, '', u.href);
}

// FNV-1a of a string, as 8 hex digits: compares a path across a reload without storing it.
function fnv(str) {
  let h = 0x811c9dc5;
  for (let i = 0; i < str.length; i++) h = Math.imul(h ^ str.charCodeAt(i), 0x01000193) >>> 0;
  return h.toString(16).padStart(8, '0');
}

function baseShape() {
  try {
    const p = new URL('.', document.baseURI).pathname;
    return { segments: p.split('/').filter(Boolean).length, hash: fnv(p) };
  } catch (e) {
    return { segments: null, hash: null, error: errText(e) };
  }
}

const signalRecord = (ctx, signal) => ({
  at: signal?.at ?? null,
  source: signal?.source ?? null,
  msSinceSignalAtStart: typeof signal?.arrivedPerf === 'number' ? Math.round(ctx.now() - signal.arrivedPerf) : null,
});

// read() now, then again 15 s and 40 s after the signal arrived while again(last) holds; times already past
// are skipped. Each reading records its time since the signal.
async function readings(ctx, signal, read, again) {
  const base = typeof signal?.arrivedPerf === 'number' ? signal.arrivedPerf : ctx.now();
  const list = [];
  const take = async () => {
    const r = await read();
    r.sinceSignalMs = Math.round(ctx.now() - base);
    list.push(r);
    return r;
  };
  let last = await take();
  for (const t of RE_READ_AT_MS) {
    if (!again(last)) break;
    const wait = base + t - ctx.now();
    if (wait <= 0) continue;
    await sleep(wait);
    last = await take();
  }
  return list;
}

// A file counts as present only when its body is the JSON the build wrote at that path: an HTML fallback
// page or a JSON error body served with status 200 does not.
const VERSION_FILES = [
  ['v1-only', './data/v1-only.json', j => j?.version === 'v1' && j?.file === 'v1-only'],
  ['v2-only', './data/v2-only.json', j => j?.version === 'v2' && j?.file === 'v2-only'],
  ['bulk-v1', './bulk/b-001.json', j => j?.n === 1],
  ['bulk-v2', './bulk/b-300.json', j => j?.n === 300],
];

async function readVersionFiles(ctx, keys = VERSION_FILES.map(f => f[0])) {
  const results = await Promise.all(VERSION_FILES.filter(f => keys.includes(f[0])).map(async ([key, path, ours]) => {
    const r = await getFile(path, { cache: 'no-store' });
    let present = false;
    if (r.ok) {
      try {
        present = ours(JSON.parse(r.body));
      } catch (e) {
        ctx.log(`${key}: the body is not JSON (${errText(e)})`);
      }
    }
    return [key, { ...fileRecord(r), present }];
  }));
  const files = Object.fromEntries(results);
  const present = { v1Only: files['v1-only']?.present, v2Only: files['v2-only']?.present, bulkV1: files['bulk-v1']?.present, bulkV2: files['bulk-v2']?.present };
  return { files, present };
}

// The republish signal if it has already arrived, else null, without waiting for it.
const republishedYet = ctx => Promise.race([ctx.republished, sleep(50).then(() => null)]);

const notV1 = ctx => ({
  status: 'skipped',
  summary: `This page is ${ctx.version}. The check runs on the v1 page that stayed open during the republish.`,
  data: { version: ctx.version },
});

// ---- the IndexedDB worker, driven from the main thread

function runIdbWorker(type, readyMs, resultMs) {
  return new Promise(resolve => {
    const t0 = performance.now();
    const steps = [];
    let ready = null;
    let done = false;
    let worker = null;
    let timer = 0;
    const finish = res => {
      if (done) return;
      done = true;
      clearTimeout(timer);
      const out = { type, ms: r1(performance.now() - t0), ready, steps, ...res };
      try {
        worker?.terminate();
      } catch (e) {
        out.terminateError = errText(e);
      }
      resolve(out);
    };
    try {
      worker = type === 'module' ? new Worker('./idb-worker.js', { type: 'module' }) : new Worker('./idb-worker.js');
    } catch (e) {
      finish({ started: false, error: `new Worker threw ${errText(e)}` });
      return;
    }
    timer = setTimeout(() => finish({ started: false, error: `no ready message in ${readyMs / 1000} s` }), readyMs);
    worker.addEventListener('error', ev => {
      ev.preventDefault?.();
      const what = ev?.message ? `${String(ev.message).slice(0, 200)}${ev.lineno ? ` (line ${ev.lineno})` : ''}` : 'an error event with no message';
      finish({ started: !!ready, error: ready ? `the worker reported ${what}` : `the worker did not start: ${what}` });
    });
    worker.addEventListener('messageerror', () => finish({ started: !!ready, error: 'a message could not be deserialised (messageerror)' }));
    worker.addEventListener('message', ev => {
      const m = ev.data;
      if (m?.type === 'ready' && !ready) {
        ready = { hasIndexedDB: m.hasIndexedDB === true, module: m.module === true, ms: r1(performance.now() - t0) };
        clearTimeout(timer);
        timer = setTimeout(() => finish({ started: true, error: `no result in ${resultMs / 1000} s` }), resultMs);
        worker.postMessage({ cmd: 'run', name: `zq-s1-idb-${suffix}-${type}`, n: N_RECORDS });
      } else if (m?.type === 'step') steps.push(String(m.step));
      else if (m?.type === 'result') finish({ started: true, result: m });
    });
  });
}

// Pass bar re-derived from the worker's raw counts.
function idbVerdict(run) {
  const r = run.result;
  if (!run.started) return { ok: false, why: run.error };
  if (!r) return { ok: false, why: run.error ?? 'no result' };
  if (!run.ready?.hasIndexedDB) return { ok: false, why: 'indexedDB is not defined in the worker' };
  if (run.type === 'module' && run.ready.module !== true) return { ok: false, why: 'the worker asked for as a module ran as a classic worker (top-level this was defined)' };
  const problems = [];
  if (r.error) problems.push(r.error);
  if (r.putOk !== N_RECORDS) problems.push(`${r.putOk ?? 0} of ${N_RECORDS} puts succeeded`);
  if (r.read !== N_RECORDS) problems.push(`getAll returned ${r.read ?? 'nothing'}`);
  if (r.count !== N_RECORDS) problems.push(`count() said ${r.count ?? 'nothing'}`);
  if (r.mismatches !== 0) problems.push(`${r.mismatches ?? 'unknown'} records differed from what was written`);
  if (r.delete?.ok !== true) problems.push(`deleteDatabase failed: ${r.delete?.error ?? 'no answer'}`);
  if (run.error) problems.push(run.error);
  return { ok: problems.length === 0, why: problems.join('; ') };
}

// ---- the checks

const compression = {
  id: 'platform.compression',
  title: 'Responses are compressed',
  kind: 'auto',
  what: 'Fetches data/compress.json (about 64 KB of JSON) without the cache and compares the encoded and decoded sizes in its Resource Timing entry, with the response type and Content-Encoding beside them.',
  async run(ctx) {
    const url = new URL('./data/compress.json', document.baseURI).href;
    const observed = [];
    let observer = null;
    try {
      observer = new PerformanceObserver(list => {
        for (const e of list.getEntries()) if (e.name === url) observed.push(e);
      });
      observer.observe({ type: 'resource' });
    } catch (e) {
      ctx.log(`PerformanceObserver is not usable: ${errText(e)}`);
    }
    const t0 = ctx.now();
    const r = await getFile('./data/compress.json', { cache: 'no-store' }, { buffer: true });
    const bodyBytes = r.body ? r.body.byteLength : null;
    let entry = null;
    for (let i = 0; i < 30 && r.ok && !entry; i++) {
      const fresh = [...observed, ...performance.getEntriesByName(url, 'resource')].filter(e => e.startTime >= t0 - 5);
      entry = fresh.at(-1) ?? null;
      if (!entry) await sleep(100);
    }
    observer?.disconnect();
    const timing = entry ? {
      transferSize: entry.transferSize ?? null,
      encodedBodySize: entry.encodedBodySize ?? null,
      decodedBodySize: entry.decodedBodySize ?? null,
      contentEncoding: 'contentEncoding' in entry ? entry.contentEncoding : undefined,
      nextHopProtocol: entry.nextHopProtocol ?? null,
      responseStatus: entry.responseStatus ?? null,
      deliveryType: entry.deliveryType ?? null,
      initiatorType: entry.initiatorType,
      duration: r1(entry.duration),
    } : null;
    const coding = r.headers?.['content-encoding'] ?? null;
    const data = {
      status: r.status, fetchMs: r.ms, bodyBytes, responseType: r.type ?? null, redirected: r.redirected ?? null, headers: r.headers ?? null, timing,
      entriesFound: observed.length + performance.getEntriesByName(url, 'resource').length,
      ...(r.error ? { error: r.error } : {}),
    };
    if (!r.ok) return { status: 'inconclusive', summary: `data/compress.json did not load (${r.error ?? `HTTP ${r.status}`}), so nothing was measured.`, data };
    const enc = timing?.encodedBodySize ?? 0;
    const dec = timing?.decodedBodySize ?? 0;
    const headerSays = coding && CODINGS.test(coding) ? coding : null;
    if (enc > 0 && dec > 0) {
      data.ratio = r1((enc / dec) * 100) / 100;
      if (dec !== bodyBytes) {
        return { status: 'inconclusive', summary: `The timing entry's decoded size (${dec} bytes) differs from the ${bodyBytes} bytes read, so the entry may not describe this response.`, data };
      }
      if (enc < dec * 0.8) {
        return { status: 'pass', summary: `Compressed in transit: ${kb(enc)} on the wire for ${kb(dec)} of JSON (${Math.round((enc / dec) * 100)}%)${coding ? `, Content-Encoding ${coding}` : ''}.`, data };
      }
      if (enc === dec) {
        const tr = timing.transferSize ?? 0;
        if (headerSays) return { status: 'inconclusive', summary: `The sizes are equal (${kb(dec)}) but the response says Content-Encoding ${coding}; the two readings disagree.`, data };
        if (tr > 0 && tr < dec * 0.8) return { status: 'inconclusive', summary: `The encoded and decoded sizes are equal (${kb(dec)}), but transferSize is ${kb(tr)}, which says compressed; the readings disagree.`, data };
        if (r.type !== 'basic') {
          return { status: 'inconclusive', summary: `The sizes are equal (${kb(dec)}) and no Content-Encoding is visible, but on a ${r.type ?? 'unknown'} response that header is not exposed, so a missing header is not evidence.`, data };
        }
        return { status: 'fail', summary: `Not compressed: ${kb(enc)} on the wire for ${kb(dec)} of JSON${coding ? `, Content-Encoding ${coding}` : ', no Content-Encoding header'} (a same-origin response, where the header would show).`, data };
      }
      return { status: 'inconclusive', summary: `Encoded ${enc} bytes against decoded ${dec}: neither compressed by a useful margin nor equal.`, data };
    }
    if (headerSays) {
      return { status: 'pass', summary: `Resource Timing gives no sizes${entry ? ' (zeros)' : ' (no entry)'}, but the response carried Content-Encoding ${coding}.`, data };
    }
    return {
      status: 'inconclusive',
      summary: entry
        ? `Resource Timing reports zero sizes and the response names no compression${coding ? ` (Content-Encoding ${coding})` : ''}, so this cannot tell.`
        : 'No Resource Timing entry appeared for the fetch and the response names no compression, so this cannot tell.',
      data,
    };
  },
};

const webLocks = {
  id: 'platform.web-locks',
  title: 'Web Locks',
  kind: 'auto',
  what: 'Takes a lock with ifAvailable, checks a second ifAvailable request inside it gets null, checks steal: true takes a held lock, then repeats the ifAvailable and steal steps against a lock a dedicated worker holds.',
  async run(ctx) {
    const locks = navigator.locks;
    const data = { hasLocks: !!locks, isSecureContext: window.isSecureContext };
    if (!locks || typeof locks.request !== 'function') {
      return { status: 'fail', summary: 'navigator.locks is missing, so the heartbeat lease fallback applies.', data };
    }
    const name = `zq-s1-probe-${suffix}`;
    const t0 = ctx.now();
    const main = await settle(locks.request(name, { ifAvailable: true }, async lock => {
      data.first = lock ? { granted: true, name: lock.name === name, mode: lock.mode } : { granted: false };
      if (!lock) return;
      data.inner = await locks.request(name, { ifAvailable: true }, l2 => (l2 ? { granted: true, mode: l2.mode } : { granted: false }));
      if (typeof locks.query === 'function') {
        const q = await locks.query();
        data.query = { heldOurs: q.held.filter(h => h.name === name).length, pendingOurs: q.pending.filter(p => p.name === name).length, heldTotal: q.held.length };
      }
    }), 5000);
    data.mainMs = r1(ctx.now() - t0);
    if (main.state !== 'resolved') data.mainError = main.state === 'timeout' ? 'no answer in 5 s' : errText(main.error);

    // steal: true against a lock held by a callback that never returns on its own.
    const stealName = `zq-s1-steal-${suffix}`;
    let release = () => {};
    let markGranted;
    const granted = new Promise(resolve => { markGranted = resolve; });
    const held = locks.request(stealName, lock => {
      markGranted(!!lock);
      return new Promise(resolve => { release = resolve; });
    });
    const heldEnd = held.then(() => ({ state: 'resolved' }), e => ({ state: 'rejected', name: e?.name ?? null }));
    const g = await settle(granted, 3000);
    const stolen = g.state === 'resolved' && g.value ? await settle(locks.request(stealName, { steal: true }, l => !!l), 3000) : null;
    const end = stolen ? await settle(heldEnd, 3000) : null;
    release();
    data.steal = {
      heldGranted: g.state === 'resolved' ? g.value : g.state,
      stolen: stolen ? (stolen.state === 'resolved' ? stolen.value : stolen.state === 'timeout' ? 'timeout' : errText(stolen.error)) : null,
      heldOutcome: end ? (end.state === 'resolved' ? end.value : end.state) : null,
    };

    data.crossAgent = await crossAgentLock(locks);
    const x = data.crossAgent;

    const missing = [];
    if (main.state !== 'resolved') missing.push(`the request did not complete (${data.mainError})`);
    if (!data.first?.granted) missing.push('the first ifAvailable request was not granted');
    if (data.first?.granted && data.inner?.granted !== false) missing.push(`the second ifAvailable request got ${data.inner?.granted ? 'a lock' : 'no answer'} instead of null`);
    if (data.steal.stolen !== true) missing.push('steal: true did not take the held lock');
    if (data.steal.stolen === true && data.steal.heldOutcome?.name !== 'AbortError') missing.push('the holder was not told with an AbortError when its lock was stolen');
    if (x.error) missing.push(`the cross-agent step failed: ${x.error}`);
    else {
      if (x.workerHeld !== true) missing.push('the worker did not get its lock');
      else {
        if (x.ifAvailableGotNull !== true) missing.push(`the page's ifAvailable request got ${x.ifAvailableGotNull === false ? 'a lock' : String(x.ifAvailableGotNull)} while the worker held it, so the lock manager is not shared with the worker`);
        if (x.stolen !== true) missing.push('steal: true did not take the worker\'s lock');
        else if (x.workerEnded !== 'AbortError') missing.push(`the worker's hold ended with ${x.workerEnded ?? 'nothing'}, not AbortError`);
      }
    }
    if (missing.length) return { status: 'fail', summary: `Web Locks fell short: ${missing.join('; ')}.`, data };
    return { status: 'pass', summary: `navigator.locks granted the lock, refused a second ifAvailable request inside it, and steal: true took a held lock (${data.mainMs} ms); against a dedicated worker's lock the page's ifAvailable got null and steal: true took it (the worker saw AbortError).`, data };
  },
};

// The cross-agent step: a dedicated worker holds a lock; the page's ifAvailable must get null and steal must win.
async function crossAgentLock(locks) {
  const name = `zq-s1-x-${suffix}`;
  const out = { lock: 'zq-s1-x-<run suffix>' };
  let worker;
  try {
    worker = new Worker('./locks-worker.js');
  } catch (e) {
    out.error = `new Worker threw ${errText(e)}`;
    return out;
  }
  const msgs = collector(worker, 'message', e => e.data ?? null);
  const errors = collector(worker, 'error', e => {
    e.preventDefault?.();
    return e?.message ? String(e.message).slice(0, 200) : 'an error event with no message';
  });
  try {
    const ready = await msgs.until(m => m?.type === 'ready', 4000);
    if (!ready) {
      out.error = errors.items[0] ? `the worker did not start: ${errors.items[0]}` : 'the worker sent no ready message in 4 s';
      return out;
    }
    out.workerHasLocks = ready.hasLocks === true;
    worker.postMessage({ cmd: 'hold', name });
    const held = await msgs.until(m => m?.type === 'held' || m?.type === 'no-locks', 3000);
    out.workerHeld = held?.type === 'held' ? held.granted === true : held?.type === 'no-locks' ? 'navigator.locks is missing in the worker' : 'no answer in 3 s';
    if (out.workerHeld !== true) return out;
    const avail = await settle(locks.request(name, { ifAvailable: true }, l => l === null), 3000);
    out.ifAvailableGotNull = avail.state === 'resolved' ? avail.value : avail.state === 'timeout' ? 'no answer in 3 s' : errText(avail.error);
    const stolen = await settle(locks.request(name, { steal: true }, l => !!l), 3000);
    out.stolen = stolen.state === 'resolved' ? stolen.value : stolen.state === 'timeout' ? 'no answer in 3 s' : errText(stolen.error);
    const ended = await msgs.until(m => m?.type === 'ended', 3000);
    out.workerEnded = ended ? ended.name ?? 'resolved' : null;
    return out;
  } finally {
    msgs.stop();
    errors.stop();
    worker.terminate();
  }
}

const idbWorker = {
  id: 'platform.idb-worker',
  title: 'IndexedDB inside a module worker',
  kind: 'auto',
  what: `A module worker opens an IndexedDB database, writes ${N_RECORDS} records in one transaction, reads them back, deletes the database and reports timings.`,
  async run(ctx) {
    if (typeof Worker !== 'function') return { status: 'fail', summary: 'Worker is not defined on this page.', data: { hasWorker: false } };
    const mod = await runIdbWorker('module', 5000, 10_000);
    const v = idbVerdict(mod);
    const r = mod.result;
    if (v.ok) {
      const listed = r.listedAfterDelete === true ? ' indexedDB.databases() still listed it right after the deletion.' : '';
      return {
        status: 'pass',
        summary: `A module worker (top-level this undefined) wrote ${N_RECORDS} records in one transaction in ${r.writeMs} ms, read all of them back unchanged in ${r.readMs} ms and deleted the database (${r.totalMs} ms in all).${listed}`,
        data: { module: mod },
      };
    }
    if (!mod.started) {
      ctx.log(`the module worker did not start (${mod.error}); trying a classic worker for comparison`);
      const classic = await runIdbWorker('classic', 4000, 6000);
      const cv = idbVerdict(classic);
      return {
        status: 'fail',
        summary: `The module worker did not start (${clip(mod.error ?? 'no reason given', 120)}). A classic worker ${cv.ok ? 'ran the IndexedDB steps correctly' : `also failed: ${clip(cv.why, 120)}`}.`,
        data: { module: mod, classic },
      };
    }
    return { status: 'fail', summary: `IndexedDB in the module worker failed: ${clip(v.why, 220)}.`, data: { module: mod } };
  },
};

const storageEstimate = {
  id: 'platform.storage-estimate',
  title: 'navigator.storage.estimate()',
  kind: 'auto',
  what: 'Reads the usage and quota from navigator.storage.estimate() and whether storage is persisted; never calls persist(), which may prompt.',
  async run() {
    const s = navigator.storage;
    const data = { hasStorage: !!s, hasEstimate: typeof s?.estimate === 'function', hasPersisted: typeof s?.persisted === 'function' };
    if (data.hasEstimate) {
      const e = await settle(Promise.resolve().then(() => s.estimate()), 5000);
      if (e.state === 'resolved') {
        const { usage, quota, usageDetails } = e.value ?? {};
        Object.assign(data, {
          usageBytes: usage ?? null,
          quotaBytes: quota ?? null,
          usageMB: typeof usage === 'number' ? r1(usage / 1048576) : null,
          quotaMB: typeof quota === 'number' ? r1(quota / 1048576) : null,
          ...(usageDetails ? { usageDetails } : {}),
        });
      } else data.estimateError = e.state === 'timeout' ? 'no answer in 5 s' : errText(e.error);
    }
    if (data.hasPersisted) {
      const p = await settle(Promise.resolve().then(() => s.persisted()), 5000);
      if (p.state === 'resolved') data.persisted = p.value;
      else data.persistedError = p.state === 'timeout' ? 'no answer in 5 s' : errText(p.error);
    }
    const parts = [];
    if (!data.hasEstimate) parts.push('navigator.storage.estimate is not available');
    else if (data.estimateError) parts.push(`estimate() failed: ${data.estimateError}`);
    else parts.push(`usage ${data.usageMB ?? '?'} MB of a ${data.quotaMB ?? '?'} MB quota`);
    if (!data.hasPersisted) parts.push('persisted() is not available');
    else if (data.persistedError) parts.push(`persisted() failed: ${data.persistedError}`);
    else parts.push(`persisted: ${data.persisted}`);
    const text = parts.join('; ');
    return { status: 'info', summary: `${text.charAt(0).toUpperCase()}${text.slice(1)}.`, data };
  },
};

const inlineStyle = {
  id: 'platform.inline-style',
  title: 'Inline style attributes through innerHTML',
  kind: 'auto',
  what: 'Parses a span with a style attribute through innerHTML, sets another span\'s colour through element.style, and reads both back with getComputedStyle.',
  async run(ctx) {
    const violations = [];
    const onViolation = e => violations.push({
      directive: e.violatedDirective ?? null,
      effective: e.effectiveDirective ?? null,
      blocked: ['inline', 'eval'].includes(e.blockedURI) ? e.blockedURI : 'other',
      disposition: e.disposition ?? null,
    });
    document.addEventListener('securitypolicyviolation', onViolation);
    try {
      const baseline = el('span', { text: 'x' });
      const parsed = el('span');
      const cssom = el('span', { text: 'x' });
      ctx.mount.replaceChildren(el('p', {}, 'Baseline ', baseline, ', innerHTML ', parsed, ', element.style ', cssom));
      // A fixed literal, no external input: this check measures the innerHTML path that KaTeX output needs.
      parsed.innerHTML = '<span style="color: rgb(1, 2, 3)">x</span>';
      cssom.style.color = 'rgb(4, 5, 6)';
      const inner = parsed.firstElementChild;
      const data = {
        baseline: getComputedStyle(baseline).color,
        innerHTML: {
          elementParsed: !!inner,
          attribute: inner?.getAttribute('style') ?? null,
          styleProperty: inner?.style.color ?? null,
          computed: inner ? getComputedStyle(inner).color : null,
        },
        cssom: { styleProperty: cssom.style.color, computed: getComputedStyle(cssom).color },
      };
      await sleep(100); // securitypolicyviolation is dispatched as a task
      data.violations = violations;
      if (data.baseline === 'rgb(1, 2, 3)') {
        return { status: 'inconclusive', summary: 'The page colour already equals the test colour, so the inline style cannot be told apart.', data };
      }
      const cssomText = data.cssom.computed === 'rgb(4, 5, 6)' ? 'element.style applied too' : `element.style gave ${data.cssom.computed}`;
      if (data.innerHTML.computed === 'rgb(1, 2, 3)') {
        return { status: 'pass', summary: `The style attribute parsed through innerHTML applied (computed rgb(1, 2, 3)); ${cssomText}.`, data };
      }
      const why = !inner ? 'the span was not created'
        : data.innerHTML.attribute == null ? 'the style attribute was dropped'
          : `the attribute is present but the computed colour is ${data.innerHTML.computed}${violations.length ? ', and the page reported a CSP violation' : ''}`;
      return { status: 'fail', summary: `The inline style did not apply: ${why}; ${cssomText}.`, data };
    } finally {
      document.removeEventListener('securitypolicyviolation', onViolation);
    }
  },
};

const hashRoutes = {
  id: 'platform.hash-routes',
  title: 'Hash routes with a slash',
  kind: 'auto',
  what: `Sets location.hash to ${SLASH_ROUTE} and then ${PLAIN_ANCHOR}, reads each back and waits for hashchange, then walks back over the entries it added and restores the original hash.`,
  async run(ctx) {
    const original = location.hash;
    const hc = collector(window, 'hashchange', e => ({ newHash: hashOf(e.newURL), oldHash: hashOf(e.oldURL), t: ctx.now() }));
    const ps = collector(window, 'popstate', () => ({ hash: hashLabel(location.hash), t: ctx.now() }));
    const data = { original: hashLabel(original), historyLengthBefore: history.length, steps: {} };
    let pushed = 0; // history entries this check added: each hash assignment that changed the hash
    try {
      if (original === SLASH_ROUTE || original === PLAIN_ANCHOR) {
        replaceHash('#s1-hash-start');
        data.startedFrom = '#s1-hash-start';
      }
      for (const target of [SLASH_ROUTE, PLAIN_ANCHOR]) {
        const t0 = ctx.now();
        if (location.hash !== target) pushed += 1;
        location.hash = target;
        const read = location.hash;
        const ev = await hc.until(v => v.newHash === target, 3000);
        data.steps[target] = {
          read: OUR_HASH.test(read) ? read : clip(read, 80),
          roundTrip: read === target,
          hashchange: !!ev,
          hashchangeMs: ev ? r1(ev.t - t0) : null,
          historyLength: history.length,
        };
      }
    } catch (e) {
      data.error = errText(e);
    } finally {
      // Walk back over the added entries, so no later back step lands on them, then restore the hash.
      if (pushed > 0) {
        const seen = ps.items.length;
        history.go(-pushed);
        const back = await ps.until(v => ps.items.indexOf(v) >= seen, 2000);
        data.walkedBack = { steps: pushed, popstate: !!back, hash: hashLabel(location.hash) };
      }
      try {
        if (location.hash !== original) replaceHash(original);
        data.restored = location.hash === original;
      } catch (e) {
        data.restored = false;
        data.restoreError = errText(e);
      }
      await sleep(50);
      hc.stop();
      ps.stop();
      data.historyLengthAfter = history.length;
      data.hashchangeEvents = hc.items.map(({ newHash, oldHash }) => ({ newHash, oldHash }));
      data.popstateEvents = ps.items.length;
    }
    const s = data.steps[SLASH_ROUTE];
    const p = data.steps[PLAIN_ANCHOR];
    const walked = data.walkedBack ? (data.walkedBack.popstate ? ` The check walked back ${data.walkedBack.steps} entries.` : ` Walking back ${data.walkedBack.steps} entries gave no popstate in 2 s.`) : '';
    const restored = `${data.restored ? 'The original hash was restored.' : `The original hash was not restored${data.restoreError ? ` (${data.restoreError})` : ''}.`}${walked}`;
    if (!s) return { status: 'fail', summary: `Setting location.hash failed: ${data.error ?? 'no reading'}. ${restored}`, data };
    const plain = p ? `${PLAIN_ANCHOR} ${p.roundTrip ? 'round-tripped' : `came back as ${p.read}`}${p.hashchange ? '' : ' without hashchange'}` : `${PLAIN_ANCHOR} was not tried (${data.error ?? 'stopped'})`;
    if (s.roundTrip && s.hashchange) {
      return { status: 'pass', summary: `${SLASH_ROUTE} round-tripped and hashchange fired in ${s.hashchangeMs} ms; ${plain}. ${restored}`, data };
    }
    const why = !s.roundTrip ? `${SLASH_ROUTE} came back as ${s.read}` : `${SLASH_ROUTE} round-tripped but hashchange did not fire within 3 s`;
    return { status: 'fail', summary: `${why}; ${plain}. ${restored}`, data };
  },
};

const googleFonts = {
  id: 'platform.google-fonts',
  title: 'Google Fonts load',
  kind: 'auto',
  what: 'Calls document.fonts.load() for Archivo and Source Code Pro and counts the faces it returns with status loaded; document.fonts.check() is recorded too.',
  async run(ctx) {
    if (!document.fonts || typeof document.fonts.load !== 'function') {
      return { status: 'fail', summary: 'document.fonts is not available, so font loading cannot be confirmed.', data: { hasFonts: false } };
    }
    const norm = f => String(f).replace(/^["']|["']$/g, '');
    // Until the Google Fonts stylesheet has loaded, no face is known and load() resolves [], so wait for it.
    const link = [...document.querySelectorAll('link[rel="stylesheet"]')].find(l => /^https:\/\/fonts\.googleapis\.com\//.test(l.href));
    const stylesheet = { linked: !!link, sheetAtStart: !!link?.sheet, waited: 'not needed' };
    if (link && !link.sheet) {
      const t0 = ctx.now();
      const w = await settle(new Promise((resolve, reject) => {
        link.addEventListener('load', resolve, { once: true });
        link.addEventListener('error', () => reject(new Error('error event')), { once: true });
      }), 8000);
      stylesheet.waited = w.state === 'resolved' ? 'load event' : w.state === 'timeout' ? 'no event in 8 s' : 'error event';
      stylesheet.waitMs = r1(ctx.now() - t0);
      stylesheet.sheetAfterWait = !!link.sheet;
    }
    const one = async family => {
      const spec = `16px "${family}"`;
      const t0 = ctx.now();
      const r = await settle(Promise.resolve().then(() => document.fonts.load(spec, 'Archivo Source 0123')), 8000);
      const faces = r.state === 'resolved' && Array.isArray(r.value) ? r.value : [];
      const known = [];
      document.fonts.forEach(f => { if (norm(f.family) === family) known.push(f); });
      return {
        family,
        ms: r1(ctx.now() - t0),
        load: r.state,
        ...(r.state === 'rejected' ? { loadError: errText(r.error) } : {}),
        returned: faces.length,
        returnedLoaded: faces.filter(f => f.status === 'loaded' && norm(f.family) === family).length,
        weights: [...new Set(faces.map(f => String(f.weight)))],
        known: known.length,
        knownLoaded: known.filter(f => f.status === 'loaded').length,
        check: document.fonts.check(spec),
      };
    };
    const [archivo, code] = await Promise.all([one('Archivo'), one('Source Code Pro')]);
    const data = { stylesheet, status: document.fonts.status, archivo, sourceCodePro: code };
    const ok = f => f.returnedLoaded > 0;
    const say = f => (ok(f) ? `${f.family} loaded in ${f.ms} ms`
      : f.known === 0 ? `${f.family} has no font face (the Google Fonts stylesheet ${link?.sheet ? 'loaded but defines no face for it' : stylesheet.waited === 'error event' ? 'failed to load' : 'did not load or was blocked'})`
        : `${f.family} did not load (${f.load}${f.loadError ? `: ${f.loadError}` : ''}, ${f.knownLoaded} of ${f.known} faces loaded)`);
    const summary = `${say(archivo)}; ${say(code)}.`;
    if (ok(archivo) && ok(code)) return { status: 'pass', summary, data };
    // Still loading is not a refusal: a load timeout, or a stylesheet with no event yet, cannot tell.
    const slow = f => !ok(f) && (f.load === 'timeout' || (f.known === 0 && stylesheet.waited === 'no event in 8 s'));
    if (slow(archivo) || slow(code)) return { status: 'inconclusive', summary: `${summary} The fonts were still loading after 8 s.`, data };
    return { status: 'fail', summary, data };
  },
};

const versionBefore = {
  id: 'platform.version-json-before',
  title: 'version.json before the republish',
  kind: 'auto',
  what: 'Fetches version.json with a query string and default caching, to compare with the same fetch after the republish.',
  async run(ctx) {
    const at = new Date().toISOString();
    const r = await getFile(`./version.json?t=${Date.now()}`);
    const rec = fileRecord(r);
    const data = { at, pageVersion: ctx.version, ...rec };
    if (!r.ok) return { status: 'info', summary: `version.json did not load (${r.error ?? `HTTP ${r.status}`}).`, data };
    const match = rec.version === ctx.version ? `matching this page` : `but this page is ${ctx.version}`;
    return { status: 'info', summary: `version.json says ${rec.version ?? 'no version'}, ${match} (HTTP ${r.status}, ${r.ms} ms).`, data };
  },
};

const versionFiles = {
  id: 'platform.version-files',
  title: 'Version-only files on this load',
  kind: 'auto',
  what: 'Fetches data/v1-only.json, data/v2-only.json, bulk/b-001.json and bulk/b-300.json without the cache on this load; on a v2 page it shows whether the files the second publish removed are gone and the added ones served.',
  async run(ctx) {
    const { files, present } = await readVersionFiles(ctx);
    const data = { pageVersion: ctx.version, files, present };
    const yn = v => (v ? 'present' : 'absent');
    const line = `v1-only ${yn(present.v1Only)}, b-001 ${yn(present.bulkV1)}, v2-only ${yn(present.v2Only)}, b-300 ${yn(present.bulkV2)}`;
    if (ctx.version === 'v1') return { status: 'info', summary: `On this v1 load: ${line}.`, data };
    if (ctx.version !== 'v2') return { status: 'skipped', summary: `This page is ${ctx.version}, so the files have no expected state.`, data };
    if (present.v1Only || present.bulkV1) return { status: 'fail', summary: `On a fresh v2 load a file the second publish removed is still served (${line}), so the null removals did not take effect.`, data };
    if (!present.v2Only || !present.bulkV2) return { status: 'fail', summary: `On a fresh v2 load a file the second publish added is not served (${line}).`, data };
    return { status: 'pass', summary: `On a fresh v2 load the removed files are gone and the added ones served (${line}): the null removals took effect.`, data };
  },
};

const clipboardCheck = {
  id: 'platform.clipboard',
  title: 'Copying a link',
  kind: 'manual',
  what: 'A button copies a fixed link with navigator.clipboard.writeText inside the tap, or selects it and tries execCommand when that is refused; you paste it back, and only whether it matched is kept (the copyable link of PLAN.md 8.1).',
  async run(ctx) {
    const data = { method: null, writeText: null, writeTextError: null, fallbackSelected: null, execCommand: null };
    const area = el('textarea', { class: 'copy-area', readonly: true, rows: '2', 'aria-label': 'The test link' });
    area.value = CLIP_LINK;
    area.hidden = true;
    const fallback = () => {
      area.hidden = false;
      area.focus();
      area.select();
      try {
        area.setSelectionRange(0, CLIP_LINK.length);
      } catch (e) {
        data.selectError = errText(e);
      }
      data.fallbackSelected = area.selectionStart === 0 && area.selectionEnd === CLIP_LINK.length;
      try {
        data.execCommand = document.execCommand('copy');
      } catch (e) {
        data.execCommand = `threw ${errText(e)}`;
      }
      data.method = data.execCommand === true ? 'execCommand' : 'selected for you to copy';
    };
    const btn = el('button', { type: 'button', class: 'btn', text: 'Copy the test link' });
    const tapped = new Promise(resolve => {
      btn.addEventListener('click', () => {
        btn.disabled = true;
        const cb = navigator.clipboard;
        if (!cb || typeof cb.writeText !== 'function') {
          data.writeText = 'not available';
          fallback();
          resolve();
          return;
        }
        let p;
        try {
          p = cb.writeText(CLIP_LINK); // inside the tap, before any await
        } catch (e) {
          p = Promise.reject(e);
        }
        p.then(
          () => { data.writeText = 'resolved'; data.method = 'clipboard.writeText'; resolve(); },
          e => { data.writeText = 'rejected'; data.writeTextError = e?.name ?? 'Error'; fallback(); resolve(); },
        );
      }, { once: true });
    });
    ctx.mount.replaceChildren(el('p', {}, btn), area);
    await tapped;
    const pasted = await ctx.note('Paste here what you copied (tap and hold in the box, then Paste). If the link is selected above, copy it first. Leave the box empty if nothing pastes.');
    const t = String(pasted ?? '').trim();
    Object.assign(data, { pastedLength: t.length, pastedMatches: t === CLIP_LINK });
    if (t === CLIP_LINK) return { status: 'pass', summary: `The link was copied (${data.method}) and pasted back unchanged.`, data };
    if (!t) return { status: 'inconclusive', summary: `Nothing was pasted, so the copy (${data.method ?? 'no method'}) is not confirmed.`, data };
    return { status: 'fail', summary: `What was pasted (${t.length} characters) is not the link, so the copy (${data.method ?? 'no method'}) did not work.`, data };
  },
};

const externalLink = {
  id: 'platform.external-link',
  title: 'An external link opens from the frame',
  kind: 'manual',
  what: 'Shows a real link to example.org with target _blank and asks what tapping it did; this decides the handoff link of ASSESSMENT.md 14.3.',
  async run(ctx) {
    const data = { clicks: 0, defaultPrevented: null, hiddenAfterClick: false, blurAfterClick: false };
    let clickedAt = null;
    const a = el('a', { class: 'btn', href: EXTERNAL_URL, target: '_blank', rel: 'noopener', text: 'Open example.org' });
    a.addEventListener('click', e => {
      data.clicks += 1;
      clickedAt = ctx.now();
      setTimeout(() => { data.defaultPrevented = e.defaultPrevented; }, 0); // after every listener has run
    });
    const onVis = () => { if (clickedAt !== null && document.visibilityState === 'hidden') data.hiddenAfterClick = true; };
    const onBlur = () => { if (clickedAt !== null) data.blurAfterClick = true; };
    document.addEventListener('visibilitychange', onVis);
    window.addEventListener('blur', onBlur);
    ctx.mount.replaceChildren(el('p', {}, a));
    try {
      const answer = await ctx.ask('Tap the example.org link in this card. What happened?', LINK_CHOICES);
      data.answer = answer;
      if (answer === LINK_CHOICES[2]) {
        if (data.clicks === 0) return { status: 'inconclusive', summary: 'Nothing happened, but no click reached the link, so the tap may not have landed on it. Run again and tap the link itself.', data };
        return { status: 'fail', summary: `Tapping the link did nothing (${data.clicks} click events reached the page).`, data };
      }
      if (LINK_CHOICES.includes(answer) && data.clicks === 0) {
        return { status: 'inconclusive', summary: `You saw a page open, but no click reached the link, so something else may have opened it.`, data };
      }
      if (LINK_CHOICES.includes(answer)) return { status: 'pass', summary: `${answer}. The handoff link of ASSESSMENT.md 14.3 can be an anchor.`, data };
      return { status: 'inconclusive', summary: `The answer was not one of the choices: ${clip(answer, 60)}.`, data };
    } finally {
      document.removeEventListener('visibilitychange', onVis);
      window.removeEventListener('blur', onBlur);
    }
  },
};

const windowOpen = {
  id: 'platform.window-open',
  title: 'window.open from a tap',
  kind: 'manual',
  what: 'A button calls window.open inside its click handler; the check records whether it returned null and asks what happened.',
  async run(ctx) {
    const data = { clicked: false };
    let win = null;
    const btn = el('button', { type: 'button', class: 'btn', text: 'Open example.org with window.open' });
    const clicked = new Promise(resolve => {
      btn.addEventListener('click', () => {
        data.clicked = true;
        try {
          win = window.open(OPEN_URL, '_blank'); // inside the click handler, before any await
          data.returnedNull = win === null;
        } catch (e) {
          data.threw = errText(e);
        }
        try {
          data.closedAtOnce = win ? win.closed : null;
        } catch (e) {
          data.closedError = errText(e);
        }
        btn.disabled = true;
        resolve();
      }, { once: true });
    });
    ctx.mount.replaceChildren(el('p', {}, btn));
    await clicked;
    const answer = await ctx.ask('What happened when you tapped the button?', OPEN_CHOICES);
    data.answer = answer;
    try {
      data.closedAtAnswer = win ? win.closed : null;
    } catch (e) {
      data.closedError = errText(e);
    }
    const ret = data.threw ? `threw ${data.threw}` : data.returnedNull ? 'returned null' : 'returned a window';
    return { status: 'info', summary: `window.open ${ret}; you saw: ${answer}.`, data };
  },
};

const fileInput = {
  id: 'platform.file-input',
  title: 'A file input',
  kind: 'manual',
  what: 'Shows a file input; when a file is chosen it reads the size and the first 64 bytes with FileReader. Only the name length, size and type are kept.',
  async run(ctx) {
    const data = { changeEvents: 0, cancelEvents: 0 };
    const input = el('input', { type: 'file', id: `platform-file-${suffix}`, 'aria-label': 'Choose any small file' });
    const giveUp = el('button', { type: 'button', class: 'btn', text: 'The picker did not open' });
    input.addEventListener('cancel', () => {
      data.cancelEvents += 1;
      ctx.log('the picker was cancelled; choose a file or tap "The picker did not open"');
    });
    const outcome = new Promise(resolve => {
      input.addEventListener('change', () => {
        data.changeEvents += 1;
        const f = input.files?.[0];
        if (f) resolve({ file: f });
        else ctx.log('change fired with no file; still waiting');
      });
      giveUp.addEventListener('click', () => resolve({ gaveUp: true }), { once: true });
    });
    ctx.mount.replaceChildren(
      el('p', { text: 'Choose any small file that is not empty. Only its size, type and the length of its name are kept.' }),
      el('p', {}, input),
      el('p', {}, giveUp),
    );
    const o = await outcome;
    giveUp.disabled = true;
    if (o.gaveUp) return { status: 'fail', summary: 'You reported that the file picker did not open.', data };
    const f = o.file;
    Object.assign(data, { nameLength: f.name.length, size: f.size, type: f.type || '(none)' });
    const expected = Math.min(64, f.size);
    const t0 = ctx.now();
    const read = await settle(new Promise((resolve, reject) => {
      const fr = new FileReader();
      fr.onload = () => resolve(fr.result);
      fr.onerror = () => reject(fr.error ?? new Error('FileReader failed'));
      fr.readAsArrayBuffer(f.slice(0, 64));
    }), 10_000);
    data.readMs = r1(ctx.now() - t0);
    input.value = '';
    if (read.state !== 'resolved') {
      data.readError = read.state === 'timeout' ? 'no answer in 10 s' : errText(read.error);
      return { status: 'fail', summary: `A file was chosen but FileReader failed: ${data.readError}.`, data };
    }
    data.bytesRead = read.value?.byteLength ?? null;
    data.expected = expected;
    if (f.size === 0) return { status: 'inconclusive', summary: 'The chosen file was empty, so reading cannot be confirmed. Run again with a file that has content.', data };
    if (data.bytesRead !== expected) return { status: 'fail', summary: `FileReader returned ${data.bytesRead} bytes where ${expected} were expected.`, data };
    return { status: 'pass', summary: `The file input worked: FileReader read the first ${expected} bytes of a ${f.size}-byte file in ${data.readMs} ms.`, data };
  },
};

const backGesture = {
  id: 'platform.back-gesture',
  title: 'The system back gesture',
  kind: 'manual',
  what: 'Pushes three history entries (#s1-back-1 to 3), asks for one back swipe, counts popstate events and reads the hash, then restores the history. If the page reloaded during the last try, it asks what the swipe did instead.',
  async run(ctx) {
    const reloaded = ctx.session.get(BACK_RELOADED_KEY);
    const data = { reloadedDuringCheck: !!reloaded, historyLengthBefore: history.length };
    const first = reloaded
      ? await ctx.ask('Last time the page reloaded during this check. What did the swipe do?', BACK_AFTER_RELOAD)
      : await ctx.ask('This check asks for one back swipe from the left edge. If you already know the swipe closes or leaves the probe, say so instead.', BACK_PRE);
    data.firstAnswer = first;
    ctx.session.set(BACK_RELOADED_KEY, null);
    if (first === BACK_AFTER_RELOAD[0] || first === BACK_PRE[1]) {
      return { status: 'fail', summary: `The back gesture leaves the probe instead of walking its history (as you saw${reloaded ? ' when the page reloaded during the last try' : ' before'}).`, data };
    }
    if (first === BACK_AFTER_RELOAD[1]) {
      return { status: 'fail', summary: 'The back gesture reloaded the probe instead of walking its history.', data };
    }
    const before = location.hash;
    const pops = collector(window, 'popstate', e => ({ hash: hashLabel(location.hash), state: e.state?.s1back ?? null, t: ctx.now() }));
    data.before = hashLabel(before);
    try {
      ctx.session.set(BACK_KEY, { at: new Date().toISOString(), version: ctx.version });
      try {
        for (let i = 1; i <= 3; i++) history.pushState({ s1back: i }, '', `#s1-back-${i}`);
      } catch (e) {
        data.pushError = errText(e);
        return { status: 'fail', summary: `history.pushState failed: ${data.pushError}.`, data };
      }
      data.afterPush = { hash: hashLabel(location.hash), historyLength: history.length };
      const answer = await ctx.ask('Swipe back from the left edge once. Then tap what happened.', BACK_CHOICES);
      data.answer = answer;
      data.popstateCount = pops.items.length;
      data.popstates = pops.items.slice(0, 10).map(({ hash, state }) => ({ hash, state }));
      data.afterAnswer = { hash: hashLabel(location.hash), state: history.state?.s1back ?? null, historyLength: history.length };

      // Restore: walk back to the entry before the three pushes, or rewrite the hash if we are not on one of them.
      const n = history.state?.s1back;
      const restore = {};
      if (Number.isInteger(n) && n >= 1 && n <= 3) {
        const seen = pops.items.length;
        history.go(-n);
        restore.went = -n;
        restore.popstate = !!(await pops.until(v => pops.items.indexOf(v) >= seen, 2000));
      }
      if (location.hash !== before) {
        try {
          replaceHash(before);
          restore.replaced = true;
        } catch (e) {
          restore.replaceError = errText(e);
        }
      }
      restore.ok = location.hash === before;
      data.restore = restore;

      const wentBack = data.popstateCount >= 1 && data.afterAnswer.hash === '#s1-back-2';
      if (answer === BACK_CHOICES[0]) {
        if (wentBack) return { status: 'pass', summary: `The back gesture walked the frame's history: ${data.popstateCount} popstate, the hash went from #s1-back-3 to #s1-back-2.`, data };
        return { status: 'inconclusive', summary: `You saw one step back, but the page recorded ${data.popstateCount} popstate events and the hash ${data.afterAnswer.hash}.`, data };
      }
      if (answer === BACK_CHOICES[1]) {
        return { status: 'fail', summary: `The back gesture left the probe instead of walking its history (${data.popstateCount} popstate events were recorded).`, data };
      }
      if (answer === BACK_CHOICES[2]) {
        if (data.popstateCount === 0) return { status: 'fail', summary: 'The back gesture did nothing in the frame: no popstate event and the hash stayed #s1-back-3.', data };
        return { status: 'inconclusive', summary: `You saw nothing happen, but the page recorded ${data.popstateCount} popstate events (hash ${data.afterAnswer.hash}).`, data };
      }
      return { status: 'inconclusive', summary: `The answer was not one of the choices: ${clip(answer, 60)}.`, data };
    } finally {
      pops.stop();
      ctx.session.set(BACK_KEY, null);
    }
  },
};

const versionAfter = {
  id: 'platform.version-json-after',
  title: 'version.json after the republish',
  kind: 'republish',
  what: 'After the republish signal, fetches version.json with a fresh query string and default caching, then with no-store, again 15 s and 40 s after the signal while it says v1; v2 means it is not cached, and data/v2-only.json separates a cached version.json from version scoping.',
  async run(ctx) {
    const signal = await ctx.republished;
    if (ctx.version !== 'v1') return notV1(ctx);
    const read = async () => ({
      defaultCache: fileRecord(await getFile(`./version.json?t=${Date.now()}`)),
      noStore: fileRecord(await getFile(`./version.json?t=${Date.now()}-ns`, { cache: 'no-store' })),
    });
    const list = await readings(ctx, signal, read, r => r.defaultCache.version === 'v1');
    const last = list.at(-1);
    const { defaultCache: def, noStore: fresh } = last;
    const data = {
      at: new Date().toISOString(), pageVersion: ctx.version, signal: signalRecord(ctx, signal),
      readings: list.map(r => ({ sinceSignalMs: r.sinceSignalMs, defaultCache: r.defaultCache.version, noStore: r.noStore.version })),
      defaultCache: def, noStore: fresh,
    };
    const when = `${(last.sinceSignalMs / 1000).toFixed(1)} s after the signal`;
    const later = list.length > 1 ? ` The first reading said ${list[0].defaultCache.version ?? 'nothing'}; this is reading ${list.length}, ${when}.` : '';
    if (def.version === 'v2') {
      return { status: 'pass', summary: `version.json says v2 with a fresh query string and default caching, so it is not cached (HTTP ${def.status}, ${def.ms} ms).${later}`, data };
    }
    if (def.version === 'v1' && fresh.version === 'v2') {
      return { status: 'fail', summary: `version.json said v1 with default caching but v2 with no-store, ${when}: a cache between the page and the host served it despite the fresh query string.`, data };
    }
    if (def.version === 'v1' && fresh.version === 'v1') {
      const only = await readVersionFiles(ctx, ['v2-only']);
      data.v2OnlyPresent = only.present.v2Only;
      if (signal?.source === 'manual' && list.every(r => r.defaultCache.version === 'v1')) {
        return { status: 'inconclusive', summary: `version.json said v1 with default caching and with no-store at every reading, the last ${when}, and the signal was started by hand, so v2 may not have been live.`, data };
      }
      if (only.present.v2Only) {
        return { status: 'fail', summary: `version.json said v1 with default caching and with no-store, ${when}, while data/v2-only.json is served: the host served a cached version.json despite the query string.`, data };
      }
      return { status: 'inconclusive', summary: `version.json said v1 with default caching and with no-store, ${when}, and data/v2-only.json is not served: this open page reads its own version's files (see platform.version-scoping), so caching cannot be judged here.`, data };
    }
    if (def.version === 'v1') {
      return { status: 'inconclusive', summary: `version.json said v1 with default caching ${when}; the no-store fetch gave ${fresh.version ?? `no version (HTTP ${fresh.status ?? 'none'})`}, so the cause cannot be told.`, data };
    }
    return { status: 'inconclusive', summary: `version.json gave no version (HTTP ${def.status ?? 'none'}${def.error ? `, ${def.error}` : ''}), so caching cannot be judged.`, data };
  },
};

const versionScoping = {
  id: 'platform.version-scoping',
  title: 'Version scoping after the republish',
  kind: 'republish',
  what: 'After the republish signal, fetches data/v1-only.json and data/v2-only.json (and bulk/b-001.json and bulk/b-300.json) without the cache, again 15 s and 40 s after the signal while only v1\'s files show, and records which exist.',
  async run(ctx) {
    const signal = await ctx.republished;
    if (ctx.version !== 'v1') return notV1(ctx);
    const list = await readings(ctx, signal, () => readVersionFiles(ctx), r => r.present.v1Only && !r.present.v2Only);
    const last = list.at(-1);
    const f = last.files;
    const { v1Only: v1, v2Only: v2, bulkV1: b1, bulkV2: b2 } = last.present;
    const changed = list.some(r => r.present.v1Only !== list[0].present.v1Only || r.present.v2Only !== list[0].present.v2Only);
    const data = {
      at: new Date().toISOString(), pageVersion: ctx.version, signal: signalRecord(ctx, signal),
      readings: list.map(r => ({ sinceSignalMs: r.sinceSignalMs, present: r.present })),
      files: f, present: last.present, changedBetweenReadings: changed,
    };
    const when = `${(last.sinceSignalMs / 1000).toFixed(1)} s after the signal`;
    const statuses = `v1-only HTTP ${f['v1-only'].status ?? 'none'}, v2-only HTTP ${f['v2-only'].status ?? 'none'}`;
    const bulk = b1 === v1 && b2 === v2 ? 'the bulk files agree' : `the bulk files disagree (b-001 ${b1 ? 'present' : 'absent'}, b-300 ${b2 ? 'present' : 'absent'})`;
    const delay = changed ? ` The first reading differed: the new version took up to ${when} to reach this page.` : '';
    if (v1 && !v2 && signal?.source === 'manual' && !changed) {
      return { status: 'inconclusive', summary: `This open v1 page still reads v1's files ${when}, but the signal was started by hand, so v2 may not have been live (${statuses}; ${bulk}).`, data };
    }
    let reads;
    if (v1 && !v2) reads = `This open v1 page still reads v1's files ${when}: its paths are scoped to the version it loaded`;
    else if (!v1 && v2) reads = 'This open v1 page now reads v2\'s files: its paths follow the latest publish';
    else if (v1 && v2) reads = 'This open v1 page reads both versions\' files: the removed v1 file is still served and the new v2 file appears';
    else reads = 'This open v1 page reads neither version-only file';
    return { status: 'info', summary: `${reads} (${statuses}; ${bulk}).${delay}`, data };
  },
};

const reload = {
  id: 'platform.reload',
  title: 'location.reload() after the republish',
  kind: 'manual',
  what: 'After the republish signal, stores a marker and calls location.reload(); when the page loads again it reports which version loaded.',
  async run(ctx) {
    const signal = await republishedYet(ctx);
    if (!signal) return { status: 'skipped', summary: 'The republish signal has not arrived on this page yet. Run this after it arrives.', data: { version: ctx.version } };
    const go = await ctx.ask('This reloads the page with location.reload(). Results already saved to db are kept; if db is not connected, tap Copy results first. Reload now?', ['Reload now', 'Not now']);
    if (go !== 'Reload now') return { status: 'skipped', summary: 'You chose not to reload yet. Run again when ready.', data: { version: ctx.version } };
    const marker = { from: ctx.version, at: new Date().toISOString(), base: baseShape() };
    // Both carriers, always: sessionStorage may not survive a reload the host turns into a new frame.
    const carriers = { session: ctx.session.set(RELOAD_KEY, marker), hash: false };
    try {
      replaceHash(`#s1-reload-${['v1', 'v2'].includes(ctx.version) ? ctx.version : 'unknown'}`);
      carriers.hash = true;
    } catch (e) {
      ctx.log(`the URL hash cannot carry the marker: ${errText(e)}`);
    }
    if (!carriers.session && !carriers.hash) {
      return { status: 'error', summary: 'Neither sessionStorage nor the URL hash can carry the marker across a reload.', data: { error: 'no carrier', marker: { from: marker.from, at: marker.at } } };
    }
    ctx.log(`marker stored (sessionStorage ${carriers.session}, hash ${carriers.hash}); waiting 3 s so the latest results reach db, then calling location.reload()`);
    await sleep(3000);
    location.reload();
    await sleep(10_000);
    // Still running: the reload did not happen.
    ctx.session.set(RELOAD_KEY, null);
    try {
      if (RELOAD_HASH.test(location.hash)) replaceHash('');
    } catch (e) {
      ctx.log(`could not clear the hash marker: ${errText(e)}`);
    }
    return { status: 'fail', summary: 'location.reload() was called but the page did not reload within 10 s.', data: { marker: { from: marker.from, at: marker.at }, carriers } };
  },
};

const toolCheck = (id, title, what) => ({
  id,
  title,
  kind: 'tool',
  what,
  async run() {
    return { status: 'info', summary: 'Claude records this from the publishing tool' };
  },
});

// ---- resume: results that finish across a reload

async function resume(ctx) {
  const out = {};
  const stored = ctx.session.get(RELOAD_KEY);
  const fromHash = RELOAD_HASH.exec(location.hash);
  if (stored || fromHash) {
    const carriers = { session: !!stored, hash: !!fromHash };
    if (stored) ctx.session.set(RELOAD_KEY, null);
    if (fromHash) {
      try {
        replaceHash('');
      } catch (e) {
        ctx.log(`could not clear the hash marker: ${errText(e)}`);
      }
    }
    const marker = stored ?? { from: fromHash[1], at: null };
    const vj = fileRecord(await getFile(`./version.json?t=${Date.now()}`, { cache: 'no-store' }));
    const at = typeof marker.at === 'string' ? Date.parse(marker.at) : NaN;
    const now = baseShape();
    const basePath = marker.base?.hash ? { segmentsBefore: marker.base.segments ?? null, segmentsAfter: now.segments, same: marker.base.hash === now.hash } : null;
    const baseText = !basePath ? ' The base path was not carried across the reload, so it is not compared.'
      : basePath.same ? ' The page loaded from the same base path as before.'
        : ` The page loaded from a different base path (${basePath.segmentsBefore} segments before, ${basePath.segmentsAfter} now), direct evidence that versions are scoped by URL.`;
    out['platform.reload'] = {
      status: 'info',
      summary: `After the republish, location.reload() loaded ${ctx.version} (the page was ${marker.from ?? 'unknown'} before; version.json now says ${vj.version ?? 'nothing'}).${baseText}`,
      data: { from: marker.from ?? null, loaded: ctx.version, markedAt: marker.at ?? null, msSinceMark: Number.isNaN(at) ? null : Date.now() - at, carriers, carrier: stored ? 'sessionStorage' : 'hash', basePath, versionJson: vj },
    };
  }
  const back = ctx.session.get(BACK_KEY);
  if (back) {
    ctx.session.set(BACK_KEY, null);
    ctx.session.set(BACK_RELOADED_KEY, { at: back.at ?? null });
    const hashNow = hashLabel(location.hash);
    if (/^#s1-back-[1-3]$/.test(location.hash)) {
      try {
        replaceHash('');
      } catch (e) {
        ctx.log(`could not clear the back-gesture hash: ${errText(e)}`);
      }
    }
    out['platform.back-gesture'] = {
      status: 'inconclusive',
      summary: 'The page loaded again while the back-gesture check was waiting for your answer, so the swipe may have reloaded or reopened the probe. Tap Run again: it asks what the swipe did, without another swipe.',
      data: { pendingSince: back.at ?? null, pendingVersion: back.version ?? null, loaded: ctx.version, hashNow, reloadedFlagSet: true },
    };
  }
  return out;
}

export default {
  id: 'platform',
  title: 'Platform checks (PLAN.md stage 2 item c)',
  checks: [
    compression,
    webLocks,
    idbWorker,
    storageEstimate,
    inlineStyle,
    hashRoutes,
    googleFonts,
    versionBefore,
    versionFiles,
    externalLink,
    windowOpen,
    clipboardCheck,
    fileInput,
    backGesture,
    versionAfter,
    versionScoping,
    reload,
    toolCheck('platform.publish-omit-page', 'A publish may omit the page', 'Whether a republish that passes only changed files, without the page itself, is accepted; measured with the publishing tool.'),
    toolCheck('platform.null-removals', 'null removals and the 255-path limit', 'Whether paths passed as null to remove files count against the 255 paths of one publish; measured with the publishing tool.'),
  ],
  resume,
};
