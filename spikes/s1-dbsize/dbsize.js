// Spike S1 database size probe (docs/PLAN.md stage 2 item (d)): writes 192 KiB documents to this Artifact's
// db at a paced rate, up to 60 MiB in 320 documents, records success or the cap the store reached, then
// deletes its documents (clean-up starts by itself after 'done' or 'capped'; the button resumes it).
//
// Decision notes:
// - Pacing is start to start: a write begins pauseMs after the previous one began (2 s, so 320 writes take
//   about 11 minutes). resource_exhausted doubles the pause, up to 64 s, and retries the same document; the
//   pause never shrinks again, so a refusal is never followed by a burst. Five refusals in a row at the 64 s
//   pause stop the phase as 'error' with code 'throttled' and the refused index; Resume tries again.
// - Each body is { i, pad }, serialised to exactly 196,608 bytes and measured with TextEncoder before every
//   write. pad is a seeded base-36 sequence (about 5.17 bits a character), so no two documents are alike;
//   gzip and brotli shrink it to about two thirds [measured in Node: 0.658 and 0.656]. If the store counted
//   compressed bytes, the 60 MiB run would hold about 40 MiB; the app's JSON compresses better than this
//   pad, so a cap read in logical bytes here stays conservative for the app.
// - status/s1-size is written after every 5 documents (every 10 during clean-up) and at every state change,
//   one write at a time through one queue. It is padded to a fixed 6,144 bytes, so a status write at the
//   size cap never makes the document larger.
// - Bodies are deterministic, so after a reload the run carries on from the saved count and rewrites, with
//   identical content, the few documents written after the last status write. Clean-up deletes indices 1 to
//   docsWritten + 5, then lists the collection and deletes whatever is left until a listing comes back empty;
//   only then is the state 'clean'.
// - unavailable and unknown codes are retried once after a short random delay (db.d.ts); quota_exceeded ends
//   the run as 'capped'; every other code, and a call with no answer in 90 s, stops the phase as 'error' with
//   the code recorded. Resume after an error tries the same document again, after waiting (at most 30 s)
//   for a call that timed out to settle, so two writes to one document never overlap.
// - The saved status is db data, so it is checked field by field before the page uses it: outside a test
//   run it may not raise the 320-document ceiling or lower the pacing below the defaults. A status read that
//   is not server-definitive (fromCache) is read again before Start is offered, and clean-up ends only on an
//   empty listing that is server-definitive with no pending writes.

const DOC_BYTES = 196_608;
const DEFAULT_PAUSE_MS = 2000;
const DEFAULT_MAX_DOCS = 320;
const MAX_PAUSE_MS = 64_000;
const CLEAN_PAUSE_MS = 300;
const SPARE = 5;
const STATUS_EVERY = 5;
const CLEAN_STATUS_EVERY = 10;
const STATUS_BYTES = 6144;
const STATUS_PATH = 'status/s1-size';
const COLLECTION = 'probe';
const MAX_EVENTS = 16;
const TEXT_MAX = 300;
const MIB = 1_048_576;
const STATES = ['idle', 'running', 'paused', 'done', 'capped', 'error', 'cleaning', 'clean'];
const KNOWN_CODES = new Set(['invalid_argument', 'resource_exhausted', 'quota_exceeded', 'unavailable', 'revoked',
  'not_granted', 'capability_disabled', 'capability_removed', 'transform_error']);

// Test pacing: a number on globalThis replaces the default, read once at load.
const testPace = globalThis.__S1_TEST_PACE_MS;
const testMax = globalThis.__S1_TEST_MAX_DOCS;
const testMaxPause = globalThis.__S1_TEST_MAX_PAUSE_MS;
const TEST_PACE = typeof testPace === 'number' && Number.isFinite(testPace) && testPace >= 0 && testPace <= MAX_PAUSE_MS ? testPace : null;
const TEST_MAX = Number.isInteger(testMax) && testMax >= 1 && testMax <= 9999 - SPARE ? testMax : null;
const TEST_MAX_PAUSE = typeof testMaxPause === 'number' && Number.isFinite(testMaxPause) && testMaxPause >= 1 && testMaxPause <= MAX_PAUSE_MS ? testMaxPause : null;
const TESTING = TEST_PACE !== null || TEST_MAX !== null || TEST_MAX_PAUSE !== null;
const BASE_PAUSE_MS = TEST_PACE ?? DEFAULT_PAUSE_MS;
const BASE_MAX_DOCS = TEST_MAX ?? DEFAULT_MAX_DOCS;
const PAUSE_CAP_MS = TEST_MAX_PAUSE ?? MAX_PAUSE_MS;
const THROTTLE_LIMIT = 5; // refusals in a row at the pause cap before the phase stops
const STALE_WAIT_MS = 30_000;

const ENCODER = new TextEncoder();
const DECODER = new TextDecoder();
const ALPHABET = ENCODER.encode('0123456789abcdefghijklmnopqrstuvwxyz');
const OVERHEAD = JSON.stringify({ i: 0, pad: '' }).length - 1; // the body's bytes other than i's digits and pad

const byteLen = s => ENCODER.encode(s).length;
const iso = () => new Date().toISOString();
const docId = i => `d-${String(i).padStart(4, '0')}`;
const isInt = (v, lo, hi) => Number.isInteger(v) && v >= lo && v <= hi;
const bool = v => (typeof v === 'boolean' ? v : null);
const text = (v, max = TEXT_MAX) => (typeof v === 'string' ? v.slice(0, max) : null);
const mib = b => (b / MIB).toFixed(1);
const double = p => Math.min(PAUSE_CAP_MS, Math.max(1, p) * 2);
const sleep = ms => new Promise(r => setTimeout(r, ms));
const CALL_TIMEOUT_MS = 90_000;

let staleCall = null; // a store call that timed out and has not settled yet

// A store call that never answers becomes a 'timeout' error, so the phase stops and can be resumed; the call
// itself is kept, so the next phase can wait for it before touching the same document.
function withTimeout(p) {
  let id;
  const t = new Promise((_, reject) => {
    id = setTimeout(() => {
      const kept = Promise.resolve(p).then(() => 'resolved', e => dbError(e).code);
      staleCall = kept;
      kept.then(() => { if (staleCall === kept) staleCall = null; });
      reject({ code: 'timeout', message: `No answer from the store in ${CALL_TIMEOUT_MS / 1000} s.` });
    }, CALL_TIMEOUT_MS);
  });
  return Promise.race([p, t]).finally(() => clearTimeout(id));
}

// Waits, at most 30 s, for a call that timed out; resolves how it ended, or null when none is pending.
async function settleStale() {
  const kept = staleCall;
  if (!kept) return null;
  say('Waiting for the store call that timed out to finish before writing again.');
  const how = await Promise.race([kept, sleep(STALE_WAIT_MS).then(() => 'still pending after 30 s')]);
  addEvent(st.phase, null, `stale call ${how}`.slice(0, 60), null);
  return how;
}

function duration(ms) {
  const s = Math.max(0, Math.round(ms / 1000));
  return s < 60 ? `${s} s` : `${Math.floor(s / 60)} min ${s % 60} s`;
}

// Mulberry32 seeded by the document index: deterministic, so a rewrite after a reload is identical.
function padFor(i, len) {
  const out = new Uint8Array(len);
  let a = Math.imul(i, 0x9e3779b1) ^ 0x5331d0c5;
  for (let k = 0; k < len; k++) {
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    out[k] = ALPHABET[((t ^ (t >>> 14)) >>> 0) % 36];
  }
  return DECODER.decode(out);
}

function bodyFor(i) {
  const body = { i, pad: padFor(i, DOC_BYTES - OVERHEAD - String(i).length) };
  return { body, bytes: byteLen(JSON.stringify(body)) };
}

function dbError(e) {
  const code = e && typeof e.code === 'string' ? e.code : e instanceof TypeError ? 'type_error' : 'unknown';
  const message = String(e && typeof e.message === 'string' ? e.message : e).slice(0, TEXT_MAX);
  return { code, message };
}

function fresh() {
  return {
    state: 'idle', phase: 'write', outcome: null,
    docsWritten: 0, bytesWritten: 0, maxDocs: BASE_MAX_DOCS, docBytes: DOC_BYTES,
    basePauseMs: BASE_PAUSE_MS, pauseMs: BASE_PAUSE_MS, cleanPauseMs: CLEAN_PAUSE_MS,
    lastError: null, capMessage: null, refusedIndex: null,
    startedAt: null, finishedAt: null, cleanedAt: null,
    deletedCount: 0, cleanTarget: null, extraDeleted: 0, listRounds: 0, remainingAfterClean: null, finalListing: null,
    exhaustedCount: 0, retriedCount: 0, events: [],
    lastWriteMs: null, maxWriteMs: null, sumWriteMs: 0, timedWrites: 0,
    wakeLock: null, ua: null, updatedAt: null,
    testOverrides: TESTING ? { paceMs: TEST_PACE, maxDocs: TEST_MAX, maxPauseMs: TEST_MAX_PAUSE } : null,
  };
}

// The saved status is untrusted: every field the page relies on is checked; a bad one is reported, not used.
function fromSaved(raw) {
  const st = fresh();
  const bad = [];
  const take = (key, ok) => {
    if (!(key in raw)) return;
    if (ok(raw[key])) st[key] = raw[key];
    else bad.push(key);
  };
  const intOrNull = (lo, hi) => v => v === null || isInt(v, lo, hi);
  const textOrNull = v => v === null || typeof v === 'string';
  const ms = v => typeof v === 'number' && Number.isFinite(v) && v >= 0 && v <= MAX_PAUSE_MS;
  // Outside a test run (no test override on this page), a saved status cannot lift the ceiling or the pacing.
  const minPause = TESTING ? 0 : DEFAULT_PAUSE_MS;
  take('state', v => STATES.includes(v));
  take('phase', v => v === 'write' || v === 'clean');
  take('outcome', v => v === null || ['done', 'capped', 'error'].includes(v));
  take('maxDocs', v => isInt(v, 1, TESTING ? 9999 - SPARE : DEFAULT_MAX_DOCS));
  take('docsWritten', v => isInt(v, 0, st.maxDocs));
  take('bytesWritten', v => isInt(v, 0, st.maxDocs * DOC_BYTES));
  take('basePauseMs', v => ms(v) && v >= minPause);
  take('pauseMs', v => ms(v) && v >= Math.max(minPause, st.basePauseMs));
  take('cleanPauseMs', v => ms(v) && v >= (TESTING ? 0 : CLEAN_PAUSE_MS));
  take('finalListing', v => v === null || (v && typeof v === 'object' && isInt(v.size, 0, 1000)));
  take('lastError', v => v === null || (v && typeof v.code === 'string' && typeof v.message === 'string'));
  take('capMessage', textOrNull);
  take('refusedIndex', intOrNull(1, 9999));
  for (const k of ['startedAt', 'finishedAt', 'cleanedAt', 'wakeLock', 'ua', 'updatedAt']) take(k, textOrNull);
  take('deletedCount', v => isInt(v, 0, 9999));
  take('cleanTarget', intOrNull(0, 9999));
  for (const k of ['extraDeleted', 'listRounds', 'exhaustedCount', 'retriedCount', 'timedWrites']) take(k, v => isInt(v, 0, 1e9));
  take('remainingAfterClean', intOrNull(0, 1e6));
  for (const k of ['lastWriteMs', 'maxWriteMs']) take(k, v => v === null || (typeof v === 'number' && Number.isFinite(v) && v >= 0));
  take('sumWriteMs', v => typeof v === 'number' && Number.isFinite(v) && v >= 0);
  take('events', v => Array.isArray(v));
  take('testOverrides', v => v === null || (v && typeof v === 'object'));
  if (bad.length) return { st, bad };
  // Copy only known fields, bounded, so nothing unexpected from the store is written back.
  const index = v => (isInt(v, 0, 9999) ? v : text(v, 20));
  if (st.lastError) {
    const e = st.lastError;
    st.lastError = { code: text(e.code, 60), message: text(e.message), phase: text(e.phase, 10), i: index(e.i), at: text(e.at, 40) };
  }
  st.events = st.events.filter(e => e && typeof e === 'object' && typeof e.code === 'string').slice(-MAX_EVENTS)
    .map(e => ({ at: text(e.at, 40), phase: text(e.phase, 10), i: index(e.i), code: text(e.code, 60), pauseMs: ms(e.pauseMs) ? e.pauseMs : null }));
  if (st.testOverrides) {
    const t = st.testOverrides;
    st.testOverrides = { paceMs: ms(t.paceMs) ? t.paceMs : null, maxDocs: isInt(t.maxDocs, 1, 9999) ? t.maxDocs : null, maxPauseMs: ms(t.maxPauseMs) ? t.maxPauseMs : null };
  }
  if (st.finalListing) {
    const f = st.finalListing;
    st.finalListing = { size: f.size, fromCache: bool(f.fromCache), hasPendingWrites: bool(f.hasPendingWrites), at: text(f.at, 40) };
  }
  for (const k of ['capMessage', 'startedAt', 'finishedAt', 'cleanedAt', 'wakeLock', 'ua', 'updatedAt']) st[k] = text(st[k]);
  if (st.wakeLock === 'held') st.wakeLock = 'held before the page closed';
  return { st, bad };
}

// ---- state

let db = null;
let st = fresh();
let active = false;       // a write or clean-up loop is running in this page
let stopAsked = false;    // Pause was tapped; the write loop stops at its next checkpoint
let wakeTimer = null;     // resolves the current pacing wait early when Pause is tapped
let badSaved = null;      // the saved status failed its checks: only clean-up is offered
let loadFailed = false;
let lastSaved = null;     // the last body status/s1-size accepted, without its reserve
let lastSavedAt = null;
let statusError = null;
let consecutive = 0;      // resource_exhausted refusals in a row
let atCapInARow = 0;      // of those, refusals that came while the pause was already at its cap
let wakeSentinel = null;
let statusQueue = Promise.resolve();
let ui = null;

function addEvent(phase, i, code, pauseMs) {
  st.events.push({ at: iso(), phase, i, code, pauseMs });
  if (st.events.length > MAX_EVENTS) st.events.splice(MAX_EVENTS / 2, 1); // keeps the first 8 and the latest 8
}

// ---- status document: one queue, fixed size

function statusBody() {
  const body = { ...st, events: st.events.map(e => ({ ...e })), lastError: st.lastError && { ...st.lastError }, updatedAt: iso(), reserve: '' };
  const used = byteLen(JSON.stringify(body));
  body.reserve = used < STATUS_BYTES ? '.'.repeat(STATUS_BYTES - used) : '';
  return body;
}

function saveStatus() {
  const body = statusBody(); // the state as it is now, even if an earlier write is still in the queue
  statusQueue = statusQueue.then(() => writeStatus(body));
  return statusQueue;
}

async function writeStatus(body) {
  for (let attempt = 1; ; attempt++) {
    try {
      await db.doc(STATUS_PATH).set(body);
      const { reserve, ...shown } = body;
      lastSaved = shown;
      lastSavedAt = body.updatedAt;
      statusError = null;
      render();
      return true;
    } catch (e) {
      const err = dbError(e);
      const retry = attempt < 4 && (err.code === 'resource_exhausted' || err.code === 'unavailable' || !KNOWN_CODES.has(err.code));
      if (!retry) {
        statusError = { ...err, at: iso() };
        console.error(`status/s1-size write failed (${err.code}): ${err.message}`);
        render();
        return false;
      }
      await sleep(1000 * 2 ** (attempt - 1));
    }
  }
}

// ---- pacing

// Waits until performance.now() reaches `until`. With `cancellable`, Pause ends the wait early: resolves false.
function waitUntil(until, cancellable) {
  const ms = until - performance.now();
  if (cancellable && stopAsked) return Promise.resolve(false);
  if (ms <= 0) return Promise.resolve(true);
  if (!cancellable) return sleep(ms).then(() => true);
  return new Promise(resolve => {
    const id = setTimeout(() => { wakeTimer = null; resolve(true); }, ms);
    wakeTimer = () => { clearTimeout(id); wakeTimer = null; resolve(false); };
  });
}

// One store call under the probe's rules. Resolves { ok: true, value, t0, ms }, { ok: false, err } or
// { ok: false, paused: true } when Pause ends a back-off wait in the write phase.
async function attempt(call, phase, i) {
  const key = phase === 'write' ? 'pauseMs' : 'cleanPauseMs';
  let retried = false;
  for (;;) {
    const t0 = performance.now();
    try {
      const value = await withTimeout(call());
      consecutive = 0;
      atCapInARow = 0;
      return { ok: true, value, t0, ms: performance.now() - t0 };
    } catch (e) {
      const err = dbError(e);
      if (err.code === 'resource_exhausted') {
        st.exhaustedCount++;
        consecutive++;
        atCapInARow = st[key] >= PAUSE_CAP_MS ? atCapInARow + 1 : 0;
        if (atCapInARow >= THROTTLE_LIMIT) {
          addEvent(phase, i, 'throttled', st[key]);
          return { ok: false, err: { code: 'throttled', message: `${THROTTLE_LIMIT} resource_exhausted refusals in a row at the ${PAUSE_CAP_MS / 1000} s pause: the store keeps refusing.` } };
        }
        st[key] = double(st[key]);
        st.lastError = { ...err, phase, i, at: iso() };
        addEvent(phase, i, err.code, st[key]);
        render();
        if (!(await waitUntil(t0 + st[key], phase === 'write'))) return { ok: false, paused: true };
        continue;
      }
      if (!retried && err.code !== 'timeout' && err.code !== 'throttled' && (err.code === 'unavailable' || !KNOWN_CODES.has(err.code))) {
        retried = true;
        st.retriedCount++;
        addEvent(phase, i, err.code, null);
        console.warn(`${phase} ${i}: ${err.code}, retrying once: ${err.message}`);
        await sleep(500 + Math.floor(Math.random() * 1000)); // not on a graded path
        continue;
      }
      addEvent(phase, i, err.code, null);
      return { ok: false, err };
    }
  }
}

// ---- wake lock

async function holdWake() {
  if (wakeSentinel && !wakeSentinel.released) return;
  if (typeof navigator.wakeLock?.request !== 'function') {
    st.wakeLock = 'not supported';
    render();
    return;
  }
  try {
    const s = await navigator.wakeLock.request('screen');
    wakeSentinel = s;
    st.wakeLock = 'held';
    s.addEventListener('release', () => {
      if (wakeSentinel !== s) return;
      wakeSentinel = null;
      st.wakeLock = 'released by the system';
      render();
    });
  } catch (e) {
    st.wakeLock = `refused: ${e?.name ?? 'Error'}: ${e?.message ?? String(e)}`.slice(0, 160);
    console.warn('Screen wake lock refused:', e);
  }
  render();
}

async function dropWake() {
  const s = wakeSentinel;
  wakeSentinel = null;
  if (!s) return;
  try {
    await s.release();
    st.wakeLock = 'released';
  } catch (e) {
    st.wakeLock = `release failed: ${e?.name ?? 'Error'}`;
    console.warn('Screen wake lock release failed:', e);
  }
}

// ---- the write phase

async function writeLoop() {
  while (st.docsWritten < st.maxDocs) {
    if (stopAsked) return stopWriting('paused');
    const i = st.docsWritten + 1;
    const { body, bytes } = bodyFor(i);
    if (bytes !== DOC_BYTES) {
      st.lastError = { code: 'size_check', message: `Document ${i} serialises to ${bytes} bytes, not ${DOC_BYTES}.`, phase: 'write', i, at: iso() };
      return stopWriting('error');
    }
    const r = await attempt(() => db.doc(`${COLLECTION}/${docId(i)}`).set(body), 'write', i);
    if (r.paused) return stopWriting('paused');
    if (!r.ok) {
      st.lastError = { ...r.err, phase: 'write', i, at: iso() };
      if (r.err.code === 'quota_exceeded') {
        st.capMessage = r.err.message;
        st.refusedIndex = i;
        return stopWriting('capped');
      }
      return stopWriting('error');
    }
    st.docsWritten = i;
    st.bytesWritten += bytes;
    st.lastWriteMs = Math.round(r.ms);
    st.maxWriteMs = Math.max(st.maxWriteMs ?? 0, st.lastWriteMs);
    st.sumWriteMs += r.ms;
    st.timedWrites++;
    render();
    if (st.docsWritten >= st.maxDocs) break;
    if (st.docsWritten % STATUS_EVERY === 0) await saveStatus();
    await waitUntil(r.t0 + st.pauseMs, true);
  }
  return stopWriting('done');
}

async function stopWriting(state) {
  st.state = state;
  if (state !== 'paused') {
    st.outcome = state;
    st.finishedAt = iso();
  }
  stopAsked = false;
  if (state !== 'done' && state !== 'capped') await dropWake(); // done and capped go straight on to clean-up
  await saveStatus();
}

// After 'done' or 'capped' the probe deletes its documents by itself (PLAN.md item (d)).
async function autoClean() {
  if (st.state !== 'done' && st.state !== 'capped') return;
  beginClean();
  await saveStatus();
  await cleanLoop();
}

// ---- clean-up

async function cleanLoop() {
  while (st.deletedCount < st.cleanTarget) {
    const i = st.deletedCount + 1;
    const r = await attempt(() => db.doc(`${COLLECTION}/${docId(i)}`).delete(), 'clean', i);
    if (!r.ok) return stopCleaning(r.err, i);
    st.deletedCount = i;
    render();
    if (i % CLEAN_STATUS_EVERY === 0) await saveStatus();
    await waitUntil(r.t0 + st.cleanPauseMs, false);
  }
  // The index sweep covers what this page wrote; a listing proves nothing else is left in the collection.
  for (let round = 0; round < 100; round++) {
    const r = await attempt(() => db.collection(COLLECTION).limit(10).get(), 'clean', null);
    if (!r.ok) return stopCleaning(r.err, null);
    st.listRounds++;
    st.remainingAfterClean = r.value.size;
    const meta = r.value.metadata;
    st.finalListing = { size: r.value.size, fromCache: bool(meta?.fromCache), hasPendingWrites: bool(meta?.hasPendingWrites), at: iso() };
    if (r.value.empty) {
      // Only a server-definitive empty listing with nothing pending proves the collection is empty.
      if (meta?.fromCache !== false || meta?.hasPendingWrites !== false) {
        render();
        await sleep(1000);
        continue;
      }
      st.state = 'clean';
      st.cleanedAt = iso();
      await dropWake();
      await saveStatus();
      return;
    }
    for (const d of r.value.docs) {
      const del = await attempt(() => db.doc(`${COLLECTION}/${d.id}`).delete(), 'clean', d.id);
      if (!del.ok) return stopCleaning(del.err, d.id);
      st.extraDeleted++;
      render();
      await waitUntil(del.t0 + st.cleanPauseMs, false);
    }
    await saveStatus();
  }
  return stopCleaning({ code: 'not_clean', message: `The collection still lists ${st.remainingAfterClean} documents after 100 rounds.` }, null);
}

async function stopCleaning(err, i) {
  st.state = 'error';
  st.lastError = { ...err, phase: 'clean', i, at: iso() };
  await dropWake();
  await saveStatus();
}

// ---- actions

async function run(loop) {
  active = true;
  say('');
  render();
  try {
    await settleStale();
    await loop();
  } catch (e) {
    console.error('The probe loop failed:', e);
    st.state = 'error';
    st.lastError = { code: 'page_error', message: String(e?.message ?? e).slice(0, TEXT_MAX), phase: st.phase, i: null, at: iso() };
    await dropWake();
    await saveStatus();
  } finally {
    active = false;
    stopAsked = false;
    render();
  }
}

function start() {
  if (!can.start()) return;
  st = fresh();
  st.state = 'running';
  st.startedAt = iso();
  st.ua = text(navigator.userAgent);
  holdWake(); // synchronously inside the tap, so it counts as a user gesture; it handles its own refusal
  run(async () => { await saveStatus(); await writeLoop(); await autoClean(); });
}

function resume() {
  if (!can.resume()) return;
  st.state = 'running';
  st.outcome = null; // a resumed run has no outcome until it stops again
  st.finishedAt = null;
  atCapInARow = 0;
  holdWake();
  run(async () => { await saveStatus(); await writeLoop(); await autoClean(); });
}

function pause() {
  if (!can.pause()) return;
  stopAsked = true;
  wakeTimer?.();
  render();
}

function beginClean() {
  st.phase = 'clean';
  st.state = 'cleaning';
  st.cleanTarget = Math.max(st.cleanTarget ?? 0, Math.min(9999, (badSaved ? st.maxDocs : st.docsWritten) + SPARE));
}

function clean() {
  if (!can.clean()) return;
  holdWake();
  beginClean();
  atCapInARow = 0;
  run(async () => { await saveStatus(); await cleanLoop(); });
}

const interrupted = () => !active && (st.state === 'running' || st.state === 'cleaning');
const can = {
  start: () => !!db && !active && !loadFailed && !badSaved && st.state === 'idle',
  pause: () => active && st.state === 'running' && !stopAsked,
  resume: () => !!db && !active && !badSaved && st.phase === 'write' && (st.state === 'paused' || st.state === 'error' || (st.state === 'running' && interrupted())),
  clean: () => !!db && !active && !loadFailed && (['done', 'capped', 'error', 'paused'].includes(st.state) || interrupted()),
};

// ---- view

function el(tag, attrs = {}, ...kids) {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'class') n.className = v;
    else if (k === 'text') n.textContent = v;
    else n.setAttribute(k, v);
  }
  n.append(...kids);
  return n;
}

function build(app) {
  const fact = (label, id) => {
    const dd = el('dd', { id });
    return [el('div', {}, el('dt', { text: label }), dd), dd];
  };
  const [rowPause, pauseDd] = fact('Current pause', 'f-pause');
  const [rowLeft, leftDd] = fact('Time left', 'f-left');
  const [rowWrite, writeDd] = fact('Write time', 'f-write');
  const [rowRefused, refusedDd] = fact('Refusals', 'f-refused');
  const [rowWake, wakeDd] = fact('Wake lock', 'f-wake');
  const [rowDeleted, deletedDd] = fact('Deleted', 'f-deleted');
  const [rowCap, capDd] = fact('Cap message', 'f-cap');
  const [rowError, errorDd] = fact('Last error', 'f-error');
  const [rowSaved, savedDd] = fact('Status saved', 'f-saved');
  const btn = (id, label, onClick, primary) => {
    const b = el('button', { id, type: 'button', class: primary ? 'btn btn-primary' : 'btn', text: label });
    b.addEventListener('click', onClick);
    return b;
  };
  const v = {
    lede: el('p', { class: 'lede' }),
    notice: el('p', { class: 'notice', id: 'instructions' }),
    testNote: el('p', { class: 'test-note', id: 'test-note' }),
    pill: el('span', { class: 'pill', id: 'state' }),
    fill: el('div', { class: 'fill' }),
    progress: el('p', { class: 'progress-text', id: 'progress' }),
    message: el('p', { class: 'message', id: 'message', 'aria-live': 'polite' }),
    savedAt: el('p', { class: 'saved-at', id: 'saved-at' }),
    json: el('pre', { class: 'json', id: 'status-json' }),
    pauseDd, leftDd, writeDd, refusedDd, wakeDd, deletedDd, capDd, errorDd, savedDd,
    rowDeleted, rowCap, rowError,
  };
  v.bar = el('div', { class: 'bar', id: 'bar', role: 'progressbar', 'aria-label': 'Documents written', 'aria-valuemin': '0' }, v.fill);
  v.start = btn('start', 'Start', start, true);
  v.pause = btn('pause', 'Pause', pause, false);
  v.resume = btn('resume', 'Resume', resume, true);
  v.clean = btn('clean', 'Clean up', clean, false);
  const details = el('details', { class: 'saved' }, el('summary', { text: 'Saved status document' }), v.savedAt, v.json);
  app.textContent = '';
  app.append(
    el('h1', { text: 'Database size probe' }),
    v.lede,
    v.notice,
    v.testNote,
    el('section', { class: 'panel', 'aria-label': 'Progress' },
      el('div', { class: 'state-row' }, el('span', { class: 'state-label', text: 'State' }), v.pill),
      v.bar,
      v.progress,
      el('dl', { class: 'facts' }, rowPause, rowLeft, rowWrite, rowRefused, rowWake, rowDeleted, rowCap, rowError, rowSaved),
      el('div', { class: 'actions' }, v.start, v.pause, v.resume, v.clean),
      v.message,
    ),
    details,
  );
  return v;
}

// The run's result in one sentence, for the clean-up states; '' when it ended some other way.
function outcomeText(total) {
  if (st.outcome === 'capped') return `The store refused document ${st.refusedIndex} with quota_exceeded after ${st.docsWritten} documents (${mib(st.bytesWritten)} MiB); the cap message is below.`;
  if (st.outcome === 'done') return `The store took all ${st.maxDocs} documents (${total}) without a cap.`;
  return '';
}

function instructions() {
  const n = st.docsWritten;
  const total = `${mib(st.maxDocs * DOC_BYTES)} MiB`;
  const minutes = Math.max(1, Math.round((st.maxDocs * st.basePauseMs) / 60_000));
  if (loadFailed) return 'The saved status could not be read, so the probe will not start or clean up. Reload the page to try again.';
  if (badSaved) return `The saved status failed its checks (${badSaved.join(', ')}). Clean up deletes every probe index up to ${st.maxDocs + SPARE} and anything else the collection lists.`;
  if (interrupted() && st.state === 'running') return `The page closed during the run. The last saved count is ${n} documents. Resume carries on from document ${n + 1}; Clean up deletes what was written.`;
  if (interrupted()) return `Clean up was interrupted at ${st.deletedCount} of ${st.cleanTarget}. Tap Clean up to carry on.`;
  switch (st.state) {
    case 'idle': return `Tap Start, then keep the Claude app in front with the screen on for about ${minutes} ${minutes === 1 ? 'minute' : 'minutes'}. The probe writes one document every ${st.basePauseMs / 1000} s and stops early if the store refuses one with a cap. You can pause at any time.`;
    case 'running': return stopAsked ? 'Pausing after the current write.' : 'Writing. Keep the Claude app in front with the screen on. If the page reloads, tap Resume and the run carries on from the last saved count.';
    case 'paused': return `Paused after document ${n}. Resume carries on from document ${n + 1}. Clean up deletes the documents written so far and ends the probe.`;
    case 'done': return `The store took all ${st.maxDocs} documents (${total}) without a cap. Clean-up starts by itself; if it does not, tap Clean up.`;
    case 'capped': return `The store refused document ${st.refusedIndex} with quota_exceeded after ${n} documents (${mib(st.bytesWritten)} MiB). The cap message below names the cap. Clean-up starts by itself; if it does not, tap Clean up.`;
    case 'error': return st.phase === 'clean'
      ? `Clean up stopped on an error at ${st.deletedCount} of ${st.cleanTarget}. Tap Clean up to carry on.`
      : st.lastError?.code === 'throttled'
        ? `The store kept refusing document ${n + 1} with resource_exhausted at the longest pause, so the run stopped after ${n} documents. Resume tries again; Clean up deletes what was written.`
        : `The run stopped on an unexpected error after ${n} documents. Resume tries document ${n + 1} again; Clean up deletes what was written.`;
    case 'cleaning': return `${outcomeText(total)} Deleting the probe documents. Keep the Claude app in front.`.trim();
    case 'clean': return `${outcomeText(total)} Every probe document is deleted, and the result stays in status/s1-size. Tell Claude the probe is finished, then confirm deleting this probe Artifact.`.trim();
    default: return '';
  }
}

function render() {
  if (!ui) return;
  const shown = interrupted() ? 'interrupted' : st.state;
  document.getElementById('app')?.setAttribute('data-state', shown);
  ui.pill.setAttribute('data-state', shown);
  ui.pill.textContent = interrupted() ? `${st.state}, stopped` : st.state;
  ui.lede.textContent = `This probe writes up to ${st.maxDocs} documents of 192 KiB, ${mib(st.maxDocs * DOC_BYTES)} MiB in all, to this Artifact's database, to find whether the store caps its size before that. Then it deletes them.`;
  ui.notice.textContent = instructions();
  ui.testNote.textContent = st.testOverrides ? `Test pacing is on: ${JSON.stringify(st.testOverrides)}. This is not a device result.` : '';
  ui.testNote.hidden = !st.testOverrides;

  const cleaning = st.phase === 'clean';
  const done = cleaning ? st.deletedCount : st.docsWritten;
  const of = cleaning ? st.cleanTarget ?? st.docsWritten + SPARE : st.maxDocs;
  ui.fill.style.width = `${of ? Math.min(100, (100 * done) / of).toFixed(2) : 0}%`;
  ui.bar.setAttribute('aria-label', cleaning ? 'Indices deleted' : 'Documents written');
  ui.bar.setAttribute('aria-valuemax', String(of));
  ui.bar.setAttribute('aria-valuenow', String(done));
  ui.progress.textContent = cleaning
    ? `${st.deletedCount} of ${of} indices deleted, ${st.extraDeleted} more found by listing. ${st.docsWritten} documents had been written.`
    : `${st.docsWritten} of ${st.maxDocs} documents, ${mib(st.bytesWritten)} of ${mib(st.maxDocs * DOC_BYTES)} MiB`;
  ui.bar.setAttribute('aria-valuetext', ui.progress.textContent);

  ui.pauseDd.textContent = `${cleaning ? st.cleanPauseMs : st.pauseMs} ms${consecutive ? `, ${consecutive} refusals in a row` : ''}`;
  const mean = st.timedWrites ? st.sumWriteMs / st.timedWrites : 0;
  ui.leftDd.textContent = cleaning || st.docsWritten >= st.maxDocs || st.state === 'capped'
    ? 'none'
    : `about ${duration((st.maxDocs - st.docsWritten) * Math.max(st.pauseMs, mean))}`;
  ui.writeDd.textContent = st.timedWrites ? `last ${st.lastWriteMs} ms, mean ${Math.round(mean)} ms, max ${st.maxWriteMs} ms` : 'none yet';
  ui.refusedDd.textContent = `${st.exhaustedCount} resource_exhausted, ${st.retriedCount} retried once`;
  ui.wakeDd.textContent = st.wakeLock ?? 'not requested';
  ui.deletedDd.textContent = `${st.deletedCount} of ${st.cleanTarget ?? 'not set'}, ${st.extraDeleted} found by listing${st.remainingAfterClean === null ? '' : `, last listing ${st.remainingAfterClean}`}`;
  ui.rowDeleted.hidden = st.phase !== 'clean';
  ui.capDd.textContent = st.capMessage ?? '';
  ui.rowCap.hidden = !st.capMessage;
  ui.errorDd.textContent = st.lastError ? `${st.lastError.code}: ${st.lastError.message}` : 'none';
  ui.savedDd.textContent = statusError
    ? `write failed (${statusError.code}): ${statusError.message}. The next save carries the latest state.`
    : lastSavedAt ? `at ${lastSavedAt}` : 'not yet';

  ui.start.disabled = !can.start();
  ui.pause.disabled = !can.pause();
  ui.pause.textContent = stopAsked ? 'Pausing' : 'Pause';
  ui.resume.disabled = !can.resume();
  ui.clean.disabled = !can.clean();
  ui.clean.textContent = st.deletedCount > 0 && st.state !== 'clean' ? 'Carry on cleaning' : 'Clean up';

  ui.savedAt.textContent = lastSaved ? `What status/s1-size holds, as last written by or read into this page (without its padding), at ${lastSavedAt}.` : 'Nothing saved yet.';
  ui.json.textContent = lastSaved ? JSON.stringify(lastSaved, null, 1) : '';
}

function say(line) {
  if (ui) ui.message.textContent = line;
}

// ---- start-up

async function loadStatus() {
  let wait = 1000;
  for (let attempt = 1; ; attempt++) {
    try {
      const snap = await db.doc(STATUS_PATH).get();
      // A cached read could say "no earlier run" while the server holds one: read again before offering Start.
      if (snap?.metadata?.fromCache !== false) {
        if (attempt >= 6) return { ok: false, err: { code: 'not_definitive', message: 'The saved status never came back from the server (every read was from a cache).' } };
        say(`The saved status came from a cache, not the server; reading again in ${wait / 1000} s.`);
        await sleep(wait);
        wait = Math.min(wait * 2, 8000);
        continue;
      }
      return { ok: true, snap };
    } catch (e) {
      const err = dbError(e);
      const retry = attempt < 5 && (err.code === 'resource_exhausted' || err.code === 'unavailable' || !KNOWN_CODES.has(err.code));
      if (!retry) return { ok: false, err };
      say(`Reading the saved status: ${err.code}, trying again in ${wait / 1000} s.`);
      await sleep(wait);
      wait *= 2;
    }
  }
}

async function main() {
  const app = document.getElementById('app');
  if (!app) throw new Error('#app is missing');
  ui = build(app);
  render();
  say('Connecting to the database.');
  let ns = null;
  try {
    ns = (await window.claude?.use?.('db')) ?? null;
  } catch (e) {
    loadFailed = true;
    render();
    say(`The database could not be reached: ${dbError(e).message}`);
    console.error('claude.use("db") failed:', e);
    return;
  }
  if (!ns) {
    loadFailed = true;
    render();
    ui.notice.textContent = 'This probe needs the Artifact\'s database, and this view does not provide it. Open the Artifact in the Claude app, signed in as its owner, and reload.';
    say('No database: the probe stops here.');
    return;
  }
  db = ns;
  const loaded = await loadStatus();
  if (!loaded.ok) {
    loadFailed = true;
    render();
    say(`The saved status could not be read (${loaded.err.code}): ${loaded.err.message}`);
    console.error('status/s1-size read failed:', loaded.err);
    return;
  }
  const raw = loaded.snap.exists ? loaded.snap.data() : undefined;
  if (raw && typeof raw === 'object' && !Array.isArray(raw)) {
    const { st: restored, bad } = fromSaved(raw);
    st = restored;
    const { reserve, ...shown } = raw;
    lastSaved = shown;
    lastSavedAt = typeof raw.updatedAt === 'string' ? raw.updatedAt : 'an unknown time';
    if (bad.length) {
      badSaved = bad;
      st.state = 'error';
      st.phase = 'clean';
      st.lastError = { code: 'bad_status', message: `Saved fields failed their checks: ${bad.join(', ')}.`, phase: 'clean', i: null, at: iso() };
    }
    say(`Loaded the saved status: ${raw.state ?? 'no state'}, ${st.docsWritten} documents written.`);
  } else {
    say('Connected. No earlier run is saved.');
  }
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible' && active && (st.state === 'running' || st.state === 'cleaning')) holdWake();
  });
  render();
}

main().catch(e => {
  console.error('The database size probe failed:', e);
  const app = document.getElementById('app');
  if (app) app.textContent = `The database size probe failed: ${String(e?.message ?? e)}`;
});
