// Spike S1 probe harness: loads the four check modules, runs their checks, shows the results and
// saves them to the Artifact's db.
//
// Decision notes:
// - Plain DOM code, no bare specifier and no HTML sink (textContent and DOM nodes only), so the harness
//   runs even when the import map, the CDN or a check module fails.
// - One serial runner: auto, tapped and republish checks share one FIFO queue, so no check measures
//   while another runs. Auto and tool checks time out at 30 s (CONTRACT.md), republish checks at 120 s
//   [our choice], and a check may declare its own `timeoutMs` (at most 300 s); manual and consent checks
//   wait for the owner with no timeout. The republish panel says done only when every republish check
//   has a result that did not come from a timeout.
// - One write pump: db writes go one at a time, each awaited, at least 1 s apart, and repeated writes to
//   one document coalesce into its latest body. A failed write shows in the header and the harness log
//   until a later write of the same document succeeds; a write that has used its retries is tried again
//   after 10 s (at most three times) and when the page is hidden.
// - db that answers after the 10 s limit is still taken: the late namespace connects, saves the run and
//   starts the republish watch.
// - The republish signal needs no clock: a v2 signal counts only when a server-definitive delivery in this
//   page showed something else first, or when its `at` differs from the v2 signal that was there when the
//   page loaded. A signal left by an earlier run cannot start the republish checks, whatever the clocks of
//   the phone and of the machine that wrote it.
// - The run document stays under 200 KB: a check's data over 16 KB becomes a marked preview, and if the
//   document is still too big the log tails go first, then the largest data fields; the document lists
//   every cut.

const STATUSES = ['pass', 'fail', 'info', 'inconclusive', 'error', 'skipped'];
const KINDS = { auto: 'Auto', manual: 'Needs you', consent: 'Asks consent', republish: 'After republish', tool: 'Claude measures' };
const TAPPABLE = new Set(['manual', 'consent', 'republish']);
const AUTO_KINDS = new Set(['auto', 'tool']);
const PILL = {
  pass: 'Pass', fail: 'Fail', info: 'Info', inconclusive: 'Inconclusive', error: 'Error', skipped: 'Skipped',
  pending: 'Not run', queued: 'Queued', running: 'Running', asking: 'Your turn', waiting: 'Waiting',
};
const PENDING_TEXT = {
  auto: 'Runs automatically.',
  tool: 'Runs automatically.',
  manual: 'Tap Run when you are ready.',
  consent: 'Tap Run. It may ask for your consent.',
  republish: 'Runs by itself when the republish signal arrives.',
};
const MODULES = [
  ['cdn', () => import('./cdn.js')],
  ['mathml', () => import('./mathml.js')],
  ['platform', () => import('./platform.js')],
  ['caps', () => import('./caps.js')],
];
const AUTO_TIMEOUT_MS = 30_000;
const REPUBLISH_TIMEOUT_MS = 120_000;
const MAX_TIMEOUT_MS = 300_000;
const LATE_RETRY_MS = 10_000;
const LATE_RETRIES = 3;
const SUMMARY_MAX = 600;
const IMPORT_TIMEOUT_MS = 30_000;
const CLAUDE_TIMEOUT_MS = 10_000;
const LOCK_TIMEOUT_MS = 15_000;
const WRITE_GAP_MS = 1_050; // 1 s plus a margin for timer jitter
const DOC_LIMIT_BYTES = 200_000;
const DATA_CAP_BYTES = 16_384;
const PREVIEW_CHARS = 2_000;
const LOG_KEEP = 300;
const NO_RETRY = new Set(['invalid_argument', 'quota_exceeded', 'revoked', 'not_granted', 'capability_disabled', 'capability_removed', 'transform_error']);
// Codes after which a fresh onSnapshot cannot help; any other code (unavailable, queue_overflow, unknown) resubscribes.
const WATCH_TERMINAL = new Set([...NO_RETRY, 'resource_exhausted']);

const pageStartEpoch = Date.now();
const harnessStart = performance.now();
const startedAt = new Date(pageStartEpoch).toISOString();
const runId = `${pageStartEpoch.toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
const runPath = `ops/s1-run-${runId}`;
const app = document.getElementById('app') ?? document.body.appendChild(document.createElement('div'));
const version = app.dataset.version ?? 'unknown';
const boot = window.__s1boot ?? null;
const utf8 = new TextEncoder();
const viewport = {
  w: window.innerWidth, h: window.innerHeight, dpr: window.devicePixelRatio,
  vw: window.visualViewport?.width ?? null, vh: window.visualViewport?.height ?? null,
  sw: window.screen?.width ?? null, sh: window.screen?.height ?? null,
};

// ---- small helpers

const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
const bytesOf = s => utf8.encode(s).length;
const clip = (s, n) => (s.length > n ? `${s.slice(0, n)}... [${s.length - n} more characters]` : s);
const stamp = () => `${((performance.now() - harnessStart) / 1000).toFixed(1)}s`;
const domId = s => s.replace(/[^A-Za-z0-9_-]/g, '-');

function errText(e) {
  if (e instanceof Error) return `${e.name}: ${e.message}`;
  if (e && typeof e === 'object') {
    if ('code' in e || 'message' in e) return `${String(e.code ?? 'error')}: ${String(e.message ?? '')}`;
    try {
      return JSON.stringify(e);
    } catch (inner) {
      return `${Object.prototype.toString.call(e)} (not serialisable: ${inner})`;
    }
  }
  return String(e);
}

function asText(v) {
  if (typeof v === 'string') return v;
  try {
    return JSON.stringify(v) ?? String(v);
  } catch (e) {
    return `${String(v)} (not serialisable: ${errText(e)})`;
  }
}

function el(tag, props = {}, ...kids) {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(props)) {
    if (v == null || v === false) continue;
    if (k === 'class') n.className = v;
    else if (k === 'text') n.textContent = v;
    else if (k.startsWith('on')) n.addEventListener(k.slice(2), v);
    else n.setAttribute(k, v === true ? '' : String(v));
  }
  for (const kid of kids.flat()) if (kid != null && kid !== false) n.append(kid);
  return n;
}

function appendLine(pre, line) {
  pre.append(`${line}\n`);
  while (pre.childNodes.length > LOG_KEEP) pre.firstChild.remove();
}

// Resolves { value } | { failed: true, error } | { timedOut: true }; ms = 0 means no timeout.
function settle(promise, ms) {
  return new Promise(resolve => {
    const timer = ms ? setTimeout(() => resolve({ timedOut: true }), ms) : 0;
    promise.then(
      value => { clearTimeout(timer); resolve({ value }); },
      error => { clearTimeout(timer); resolve({ failed: true, error }); },
    );
  });
}

function deepFreeze(o) {
  if (o && typeof o === 'object' && !Object.isFrozen(o)) {
    Object.freeze(o);
    for (const v of Object.values(o)) deepFreeze(v);
  }
  return o;
}

// ---- state

const state = {
  lock: null,
  lockError: null,
  db: null,
  dbState: 'connecting', // connecting | connected | not available
  appVersion: '',
  deviceModel: '',
  modules: {}, // id -> { ok, ms, title?, checks: [ids], error?, resumeError? }
  entries: [], // runnable checks in display order
  byId: new Map(),
  extraResults: {}, // module-load failures and invalid definitions
  truncatedIds: new Set(),
  republish: { phase: 'waiting', at: null, to: null, source: null, stale: null, sawOther: false, error: null, subscriptions: 0 },
  writes: { ok: 0, failed: 0, last: null, lastError: null, failing: {}, lateRetries: 0 },
  copy: null,
  started: false,
  autoFinished: false,
};
const ui = {};
const harnessLines = [];
let resolveRepublished;
const republished = new Promise(resolve => { resolveRepublished = resolve; });
let resolveAutoDone;
const autoDone = new Promise(resolve => { resolveAutoDone = resolve; });

function hlog(line) {
  const s = `${stamp()} ${asText(line)}`;
  harnessLines.push(s);
  if (harnessLines.length > LOG_KEEP) harnessLines.shift();
  if (ui.harnessPre) appendLine(ui.harnessPre, s);
}

const session = log => ({
  get(key) {
    try {
      const raw = window.sessionStorage.getItem(key);
      return raw == null ? null : JSON.parse(raw);
    } catch (e) {
      log(`sessionStorage read of ${key} failed: ${errText(e)}`);
      return null;
    }
  },
  set(key, value) {
    try {
      if (value === undefined || value === null) window.sessionStorage.removeItem(key);
      else window.sessionStorage.setItem(key, JSON.stringify(value));
      return true;
    } catch (e) {
      log(`sessionStorage write of ${key} failed: ${errText(e)}`);
      return false;
    }
  },
});
const harnessSession = session(hlog);
const previousRunId = harnessSession.get('s1.runId');
harnessSession.set('s1.runId', runId);

// window.claude.use(name) with a 10 s limit; resolves null when absent, refused or silent. A namespace
// that arrives after the limit goes to onLate, when given.
function useCapability(name, log, onLate) {
  const t0 = performance.now();
  const claude = window.claude;
  if (!claude || typeof claude.use !== 'function') {
    log(`window.claude.use is not available, so ${name} is null`);
    return Promise.resolve(null);
  }
  return new Promise(resolve => {
    let done = false;
    const finish = (ns, line) => {
      if (done) {
        if (ns && onLate) {
          log(`${line} (after the 10 s limit, taken late)`);
          onLate(ns);
        } else log(`${line} (after the 10 s limit, ignored)`);
        return;
      }
      done = true;
      clearTimeout(timer);
      log(line);
      resolve(ns);
    };
    const timer = setTimeout(() => finish(null, `claude.use('${name}') gave no answer in 10 s, using null`), CLAUDE_TIMEOUT_MS);
    let p;
    try {
      p = claude.use(name);
    } catch (e) {
      finish(null, `claude.use('${name}') threw ${errText(e)}`);
      return;
    }
    Promise.resolve(p).then(
      ns => finish(ns ?? null, `claude.use('${name}') resolved ${ns ? 'a namespace' : 'null'} in ${Math.round(performance.now() - t0)} ms`),
      e => finish(null, `claude.use('${name}') rejected: ${errText(e)}`),
    );
  });
}

// ---- prompts inside a card

function ask(entry, prompt, choices) {
  return new Promise(resolve => {
    const labels = (Array.isArray(choices) && choices.length ? choices : ['OK']).map(String);
    const box = el('div', { class: 'prompt', role: 'group' }, el('p', { class: 'prompt-text', text: String(prompt) }));
    const row = el('div', { class: 'prompt-choices' });
    for (const label of labels) {
      row.append(el('button', {
        type: 'button',
        class: 'btn',
        text: label,
        onclick: () => {
          box.remove();
          entry.asking = Math.max(0, (entry.asking ?? 1) - 1);
          entry.paint();
          entry.log(`asked "${clip(String(prompt), 120)}", answer "${label}"`);
          resolve(label);
        },
      }));
    }
    box.append(row);
    showPrompt(entry, box);
  });
}

let noteSeq = 0;

function note(entry, prompt) {
  return new Promise(resolve => {
    const id = `note-${domId(entry.id)}-${++noteSeq}`;
    const input = el('textarea', { id, class: 'note-input', rows: 3, autocomplete: 'off' });
    const box = el('div', { class: 'prompt', role: 'group' },
      el('label', { class: 'prompt-text', for: id, text: String(prompt) }),
      input,
      el('div', { class: 'prompt-choices' }, el('button', {
        type: 'button',
        class: 'btn btn-primary',
        text: 'Save',
        onclick: () => {
          const text = input.value;
          box.remove();
          entry.asking = Math.max(0, (entry.asking ?? 1) - 1);
          entry.paint();
          entry.log(`note saved (${text.length} characters)`);
          resolve(text);
        },
      })));
    showPrompt(entry, box);
  });
}

function showPrompt(entry, box) {
  entry.panel.prompts.append(box);
  entry.asking = (entry.asking ?? 0) + 1;
  entry.paint();
  const reduce = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
  box.scrollIntoView?.({ block: 'nearest', behavior: reduce ? 'auto' : 'smooth' });
  box.querySelector('button, textarea')?.focus({ preventScroll: true });
}

// ---- ctx

function makePanel() {
  return { lines: [], pre: el('pre', { class: 'log-lines' }), prompts: el('div', { class: 'prompts' }), mount: el('div', { class: 'mount' }) };
}

function panelLog(panel) {
  return line => {
    const s = `${stamp()} ${asText(line)}`;
    panel.lines.push(s);
    if (panel.lines.length > LOG_KEEP) panel.lines.shift();
    appendLine(panel.pre, s);
  };
}

function makeCtx(entry) {
  return {
    mount: entry.panel.mount,
    ask: (prompt, choices) => ask(entry, prompt, choices),
    note: prompt => note(entry, prompt),
    log: entry.log,
    claude: name => useCapability(name, entry.log),
    version,
    lock: state.lock,
    republished,
    session: session(entry.log),
    boot,
    now: () => performance.now(),
  };
}

// ---- results

function normalise(r) {
  if (!r || typeof r !== 'object') {
    return { status: 'error', summary: 'The check returned no result object.', data: { error: 'no result', returned: clip(asText(r), 500) } };
  }
  if (!STATUSES.includes(r.status)) {
    return { status: 'error', summary: `The check returned an unknown status: ${clip(String(r.status), 40)}.`, data: { error: 'bad status', returned: clip(asText(r), 2000) } };
  }
  const summary = typeof r.summary === 'string' && r.summary.trim() ? clip(r.summary, SUMMARY_MAX) : '(The check gave no summary.)';
  let data;
  if (r.data !== undefined) {
    try {
      data = JSON.parse(JSON.stringify(r.data));
    } catch (e) {
      return { status: 'error', summary: 'The check returned data that is not JSON-safe.', data: { error: errText(e), originalStatus: r.status, originalSummary: clip(summary, 300) } };
    }
  }
  return { status: r.status, summary, data };
}

function thrown(e) {
  return { status: 'error', summary: `The check threw ${clip(errText(e), 160)}.`, data: { error: errText(e), stack: clip(String(e?.stack ?? ''), 2000) } };
}

function previewOf(data, size) {
  return { truncated: true, bytes: size, preview: clip(JSON.stringify(data), PREVIEW_CHARS) };
}

function noteTruncation(id, size, why) {
  if (state.truncatedIds.has(id)) return;
  state.truncatedIds.add(id);
  hlog(`${id}: data of ${size} bytes cut to a preview (${why})`);
  paintHeader();
}

function record(entry, r, ms, trigger) {
  let data = r.data;
  entry.rawData = data;
  if (data !== undefined) {
    const size = bytesOf(JSON.stringify(data));
    if (size > DATA_CAP_BYTES) {
      data = previewOf(data, size);
      noteTruncation(entry.id, size, 'over the 16 KB per check');
      entry.log(`data of ${size} bytes is over 16 KB: the run document keeps a preview, the full data is below`);
    }
  }
  entry.result = { status: r.status, summary: r.summary, data, at: new Date().toISOString(), ms, trigger };
  entry.log(`${r.status}: ${r.summary}`);
  entry.paint();
  paintSummary();
  if (entry.check.kind === 'republish') paintRepublish();
  persist();
}

// The check's time limit in ms, 0 for none: its own timeoutMs, else the default for its kind.
function limitOf(check) {
  if (!AUTO_KINDS.has(check.kind) && check.kind !== 'republish') return 0;
  const own = typeof check.timeoutMs === 'number' && Number.isFinite(check.timeoutMs) && check.timeoutMs > 0 ? Math.min(check.timeoutMs, MAX_TIMEOUT_MS) : null;
  return own ?? (check.kind === 'republish' ? REPUBLISH_TIMEOUT_MS : AUTO_TIMEOUT_MS);
}

async function runCheck(entry, trigger) {
  const { check } = entry;
  const seq = ++entry.seq;
  entry.running = true;
  entry.paint();
  paintSummary();
  entry.log(`run started (${trigger})`);
  const limit = limitOf(check);
  const t0 = performance.now();
  const work = Promise.resolve().then(() => check.run(makeCtx(entry)));
  const outcome = await settle(work, limit);
  const ms = Math.round(performance.now() - t0);
  let result;
  if (outcome.timedOut) {
    result = { status: 'error', summary: `The check did not finish within ${limit / 1000} s.`, data: { error: 'timeout', timeoutMs: limit } };
    entry.awaitingLate = true;
    work.then(r => late(entry, seq, normalise(r), t0), e => late(entry, seq, thrown(e), t0));
  } else if (outcome.failed) result = thrown(outcome.error);
  else result = normalise(outcome.value);
  entry.running = false;
  record(entry, result, ms, trigger);
}

function late(entry, seq, r, t0) {
  const ms = Math.round(performance.now() - t0);
  entry.log(`finished ${ms} ms after it started, after the timeout: ${r.status}: ${r.summary}`);
  if (entry.seq !== seq || !entry.result) return;
  entry.awaitingLate = false;
  entry.result.data = { ...entry.result.data, lateResult: { status: r.status, summary: clip(r.summary, SUMMARY_MAX), ms, data: r.data } };
  entry.rawData = entry.result.data;
  entry.paint();
  if (entry.check.kind === 'republish') paintRepublish();
  persist();
}

// ---- runner

const queue = [];
let draining = false;

function enqueue(entry, trigger) {
  if (entry.queued || entry.running) return;
  entry.queued = true;
  entry.awaitingLate = false;
  entry.trigger = trigger;
  queue.push(entry);
  entry.paint();
  paintSummary();
  if (!draining) drain();
}

async function drain() {
  draining = true;
  while (queue.length) {
    const entry = queue.shift();
    entry.queued = false;
    try {
      await runCheck(entry, entry.trigger);
    } catch (e) {
      entry.running = false;
      hlog(`harness fault while running ${entry.id}: ${errText(e)}`);
      console.error(`Spike S1: harness fault while running ${entry.id}`, e);
      record(entry, thrown(e), null, entry.trigger);
    }
  }
  draining = false;
  paintSummary();
}

// ---- db persistence

const pending = new Map(); // path -> body builder; Map order is write order, a repeat keeps its place
const retries = new Map(); // path -> failed attempts of the body now queued; a newly queued body starts again
const lateTimers = new Map(); // path -> the timer of its one later try
const lateCounts = new Map(); // path -> later tries used
let pumping = false;
let lastWriteAt = -Infinity;
let holdUntil = 0;

function queueWrite(path, build) {
  if (state.dbState === 'not available') return;
  retries.delete(path);
  pending.set(path, build);
  if (state.db && !pumping) pump();
}

const persist = () => queueWrite(runPath, () => buildRunDoc().doc);

async function pump() {
  pumping = true;
  try {
    while (pending.size && state.db) {
      const wait = Math.max(lastWriteAt + WRITE_GAP_MS, holdUntil) - performance.now();
      if (wait > 0) await sleep(wait);
      const [path, build] = pending.entries().next().value;
      pending.delete(path);
      let body;
      try {
        body = build();
      } catch (e) {
        hlog(`could not build ${path}: ${errText(e)}`);
        console.error(`Spike S1: could not build ${path}`, e);
        continue;
      }
      lastWriteAt = performance.now();
      try {
        await state.db.doc(path).set(body);
        state.writes.ok += 1;
        state.writes.last = new Date().toISOString();
        retries.delete(path);
        lateCounts.delete(path);
        if (state.writes.failing[path]) {
          delete state.writes.failing[path];
          hlog(`save of ${path} succeeded after an earlier failure`);
        }
        if (state.writes.lastErrorPath === path) {
          state.writes.lastError = null;
          state.writes.lastErrorPath = null;
        }
      } catch (e) {
        writeFailed(path, build, e);
      }
      paintHeader();
    }
  } finally {
    pumping = false;
  }
}

function writeFailed(path, build, e) {
  const code = String(e?.code ?? 'unknown');
  state.writes.failed += 1;
  state.writes.lastError = `${path}: ${errText(e)}`;
  state.writes.lastErrorPath = path;
  state.writes.failing[path] = { code, at: new Date().toISOString() };
  hlog(`save of ${path} failed: ${errText(e)}`);
  console.error(`Spike S1: save of ${path} failed`, e);
  if (NO_RETRY.has(code)) return;
  const n = (retries.get(path) ?? 0) + 1;
  retries.set(path, n);
  if (n <= 2) {
    holdUntil = performance.now() + (code === 'resource_exhausted' ? 5000 : 1000 + Math.random() * 2000);
    if (!pending.has(path)) pending.set(path, build);
    hlog(`${path}: trying again after a pause (attempt ${n + 1})`);
  } else retryLater(path, build);
}

// One more try of a write that used its retries, 10 s on; at most LATE_RETRIES per path between successes.
function retryLater(path, build) {
  const used = lateCounts.get(path) ?? 0;
  if (lateTimers.has(path) || used >= LATE_RETRIES) return;
  lateCounts.set(path, used + 1);
  hlog(`${path}: trying again in ${LATE_RETRY_MS / 1000} s`);
  lateTimers.set(path, setTimeout(() => {
    lateTimers.delete(path);
    if (!state.writes.failing[path] || pending.has(path)) return;
    state.writes.lateRetries += 1;
    queueWrite(path, build);
  }, LATE_RETRY_MS));
}

// When the page is hidden (it may be closed next), every document whose last save failed is queued again.
function flushFailed() {
  for (const path of Object.keys(state.writes.failing)) {
    if (NO_RETRY.has(state.writes.failing[path].code) || pending.has(path)) continue;
    const build = path === runPath ? () => buildRunDoc().doc : path === 'ops/s1-latest' ? latestBody : null;
    if (build) {
      hlog(`page hidden: trying the save of ${path} again`);
      queueWrite(path, build);
    }
  }
}

function buildRunDoc() {
  const results = {};
  for (const e of state.entries) {
    if (e.result) results[e.id] = { ...e.result, log: e.panel.lines.slice(-12).map(l => clip(l, 240)) };
  }
  for (const [id, r] of Object.entries(state.extraResults)) results[id] = { ...r };
  const doc = {
    runId,
    version,
    ua: navigator.userAgent,
    viewport,
    startedAt,
    appVersion: state.appVersion || null,
    deviceModel: state.deviceModel || null,
    previousRunId,
    lock: state.lock ? 'loaded' : `not loaded: ${state.lockError ?? 'pending'}`,
    boot: boot ? { mapPresent: boot.mapPresent, mapCount: boot.mapCount ?? null, start: Math.round(boot.start) } : null,
    modules: state.modules,
    db: { state: state.dbState, lateMs: state.dbLate ?? null },
    republish: { ...state.republish },
    harness: { startMs: Math.round(harnessStart), writes: { ...state.writes, failing: { ...state.writes.failing } }, copy: state.copy, log: harnessLines.slice(-40).map(l => clip(l, 240)) },
    results,
  };
  return fitDoc(doc);
}

function fitDoc(doc) {
  let json = JSON.stringify(doc);
  if (bytesOf(json) <= DOC_LIMIT_BYTES) return { doc, json };
  doc.truncation = ['log tails removed to fit 200 KB'];
  for (const r of Object.values(doc.results)) delete r.log;
  doc.harness.log = doc.harness.log.slice(-10);
  json = JSON.stringify(doc);
  let total = bytesOf(json);
  if (total > DOC_LIMIT_BYTES) {
    const sized = Object.entries(doc.results)
      .map(([id, r]) => [id, r, r.data === undefined ? 0 : bytesOf(JSON.stringify(r.data))])
      .sort((a, b) => b[2] - a[2]);
    for (const [id, r, size] of sized) {
      if (total <= DOC_LIMIT_BYTES || size <= PREVIEW_CHARS + 200) break;
      r.data = previewOf(r.data, size);
      total -= size - bytesOf(JSON.stringify(r.data));
      doc.truncation.push(`${id}: data of ${size} bytes cut to a preview`);
      noteTruncation(id, size, 'to fit the 200 KB run document');
    }
    json = JSON.stringify(doc);
    if (bytesOf(json) > DOC_LIMIT_BYTES) hlog(`the run document is still ${bytesOf(json)} bytes after cutting; the save may be refused`);
  }
  return { doc, json };
}

const latestBody = () => ({ runId, version, at: new Date().toISOString() });

async function connectDb() {
  const db = await useCapability('db', hlog, ns => {
    if (state.db) return;
    state.dbLate = Math.round(performance.now() - harnessStart);
    hlog(`db arrived late, ${state.dbLate} ms after the harness started: connecting now`);
    takeDb(ns);
  });
  if (!db) {
    state.dbState = 'not available';
    pending.clear();
    paintHeader();
    paintRepublish();
    return;
  }
  takeDb(db);
}

function takeDb(db) {
  state.db = db;
  state.dbState = 'connected';
  paintHeader();
  paintRepublish();
  persist();
  queueWrite('ops/s1-latest', latestBody);
  watchRepublish(db, 0);
}

// ---- the republish signal

function parseAt(at) {
  if (typeof at === 'number' && Number.isFinite(at)) return at > 1e12 ? at : at > 1e9 ? at * 1000 : null;
  if (typeof at === 'string') {
    const t = Date.parse(at);
    return Number.isNaN(t) ? null : t;
  }
  return null;
}

function watchRepublish(db, attempt) {
  let ref;
  try {
    ref = db.doc('ops/s1-republished');
  } catch (e) {
    state.republish.error = errText(e);
    hlog(`could not watch ops/s1-republished: ${errText(e)}`);
    paintRepublish();
    return;
  }
  state.republish.subscriptions += 1;
  let unsubscribe = null;
  let stopNow = false;
  let logged = false;
  const stop = () => { if (unsubscribe) unsubscribe(); else stopNow = true; };
  const next = snap => {
    const r = state.republish;
    if (r.phase === 'arrived') return stop();
    const definitive = snap?.metadata?.fromCache === false;
    const d = snap.exists ? snap.data() : undefined;
    if (d?.to !== 'v2') {
      if (!logged) hlog(`ops/s1-republished ${snap.exists ? `says to: ${asText(d?.to)}` : 'does not exist yet'}${definitive ? '' : ' (not server-definitive)'}`);
      logged = true;
      if (definitive) r.sawOther = true;
      return;
    }
    if (!definitive) return; // a cached v2 could be any earlier signal: wait for the server's answer
    const key = asText(d.at ?? null);
    const why = r.sawOther ? 'it followed a server delivery of another value while this page was open'
      : r.stale && r.stale.key !== key ? 'its at differs from the signal that was there when this page loaded' : null;
    if (!why) {
      if (!r.stale) {
        r.stale = { at: d.at ?? null, key };
        hlog(`ops/s1-republished already said v2 (at ${key}) when this page loaded: ignored`);
        paintRepublish();
      }
      return;
    }
    const t = parseAt(d.at);
    arrive({ at: d.at ?? null, to: 'v2', source: 'db', fromCache: false, why, atAfterPageStart: t === null ? null : t > pageStartEpoch });
    stop();
  };
  const error = e => {
    const code = String(e?.code ?? 'unknown');
    state.republish.error = errText(e);
    hlog(`the watch on ops/s1-republished stopped: ${errText(e)}`);
    paintRepublish();
    if (!WATCH_TERMINAL.has(code) && attempt < 3 && state.republish.phase !== 'arrived') {
      hlog('subscribing again in 5 s');
      setTimeout(() => watchRepublish(db, attempt + 1), 5000);
    }
  };
  try {
    unsubscribe = ref.onSnapshot(next, error);
    if (stopNow) unsubscribe();
  } catch (e) {
    error(e);
  }
}

function arrive(signal) {
  if (state.republish.phase === 'arrived') return;
  state.republish = {
    ...state.republish,
    phase: 'arrived',
    at: signal.at,
    to: signal.to,
    source: signal.source,
    fromCache: signal.fromCache ?? null,
    why: signal.why ?? null,
    atAfterPageStart: signal.atAfterPageStart ?? null,
    arrivedAt: new Date().toISOString(),
    arrivedMs: Math.round(performance.now() - harnessStart),
  };
  hlog(`republish signal arrived (${signal.source}, at ${asText(signal.at)}${signal.why ? `: ${signal.why}` : ''})`);
  // arrivedPerf is this page's performance.now() at arrival, so a check can time from it with ctx.now().
  resolveRepublished({ at: signal.at, to: signal.to, source: signal.source, arrivedAt: state.republish.arrivedAt, arrivedPerf: performance.now() });
  for (const e of state.entries) if (e.check.kind === 'republish') enqueue(e, 'republish');
  for (const e of state.entries) e.paint();
  paintRepublish();
  persist();
}

// ---- modules

async function loadLock() {
  const t0 = performance.now();
  const abort = new AbortController();
  const timer = setTimeout(() => abort.abort(), LOCK_TIMEOUT_MS);
  try {
    const r = await fetch('./lock.json', { cache: 'no-store', signal: abort.signal });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    state.lock = deepFreeze(await r.json());
    hlog(`lock.json loaded in ${Math.round(performance.now() - t0)} ms`);
  } catch (e) {
    state.lockError = errText(e);
    hlog(`lock.json did not load: ${state.lockError}`);
    console.error('Spike S1: lock.json did not load', e);
  } finally {
    clearTimeout(timer);
  }
  paintHeader();
}

function checkProblems(c, modId) {
  if (!c || typeof c !== 'object') return ['it is not an object'];
  const p = [];
  if (typeof c.id !== 'string' || !c.id) p.push('it has no id');
  else if (state.byId.has(c.id)) p.push(`the id ${c.id} is used twice`);
  if (!Object.hasOwn(KINDS, c.kind)) p.push(`the kind ${String(c.kind)} is unknown`);
  if (typeof c.run !== 'function') p.push('it has no run function');
  if (typeof c.title !== 'string' || !c.title) p.push('it has no title');
  if (typeof c.id === 'string' && !c.id.startsWith(`${modId}.`)) hlog(`check id ${c.id} does not start with ${modId}.`);
  return p;
}

function moduleFailed(id, ms, error, stack) {
  state.modules[id] = { ok: false, ms, error, checks: [] };
  state.extraResults[`${id}.module-load`] = {
    status: 'error', summary: `${id}.js did not load: ${clip(error, 200)}`, data: { error, stack: clip(stack ?? '', 2000) }, at: new Date().toISOString(), ms,
  };
  hlog(`${id}.js did not load: ${error}`);
  console.error(`Spike S1: ${id}.js did not load: ${error}`);
  ui.modules.append(el('section', { class: 'module', 'aria-labelledby': `m-${id}` },
    el('h2', { class: 'module-title', id: `m-${id}`, text: `${id}.js` }),
    el('article', { class: 'card', 'data-status': 'error' },
      el('div', { class: 'card-head' }, el('h3', { class: 'card-title', text: 'The module did not load' }), el('span', { class: 'pill', 'data-status': 'error', text: PILL.error })),
      el('p', { class: 'card-summary', text: `${error}. The other modules still run.` }))));
}

function register(id, ms, outcome) {
  if (outcome.timedOut) return moduleFailed(id, ms, `the import did not finish within ${IMPORT_TIMEOUT_MS / 1000} s`);
  if (outcome.failed) return moduleFailed(id, ms, errText(outcome.error), outcome.error?.stack);
  const mod = outcome.value?.default;
  if (!mod || typeof mod !== 'object' || !Array.isArray(mod.checks)) return moduleFailed(id, ms, 'its default export has no checks array');
  if (mod.id !== id) hlog(`${id}.js says its id is ${asText(mod.id)}`);

  const panel = makePanel();
  const modEntry = { id, panel, log: panelLog(panel), paint: () => {}, seq: 0 };
  const info = { ok: true, ms, title: typeof mod.title === 'string' ? mod.title : id, checks: [] };
  state.modules[id] = info;
  const cards = [];
  mod.checks.forEach((c, i) => {
    const problems = checkProblems(c, id);
    if (problems.length) {
      const key = typeof c?.id === 'string' && c.id && !state.byId.has(c.id) && !state.extraResults[c.id] ? c.id : `${id}.invalid-${i}`;
      const summary = `The check definition is invalid: ${problems.join('; ')}.`;
      state.extraResults[key] = { status: 'error', summary, data: { error: 'invalid definition', problems }, at: new Date().toISOString(), ms: null };
      hlog(`${key}: ${summary}`);
      cards.push(el('article', { class: 'card', 'data-status': 'error' },
        el('div', { class: 'card-head' }, el('h3', { class: 'card-title', text: typeof c?.title === 'string' ? c.title : key }), el('span', { class: 'pill', 'data-status': 'error', text: PILL.error })),
        el('p', { class: 'card-summary', text: summary })));
      return;
    }
    const entry = { id: c.id, check: c, module: id, panel: makePanel(), seq: 0, queued: false, running: false, asking: 0, result: null, rawData: undefined };
    entry.log = panelLog(entry.panel);
    entry.paint = () => paintCard(entry);
    state.entries.push(entry);
    state.byId.set(c.id, entry);
    info.checks.push(c.id);
    cards.push(makeCard(entry));
  });
  hlog(`${id}.js loaded in ${ms} ms with ${info.checks.length} checks`);

  ui.modules.append(el('section', { class: 'module', 'aria-labelledby': `m-${id}` },
    el('h2', { class: 'module-title', id: `m-${id}`, text: info.title }),
    el('p', { class: 'module-meta' }, el('code', { text: `${id}.js` }), ` loaded in ${ms} ms, ${info.checks.length} checks`),
    panel.prompts,
    panel.mount,
    el('details', { class: 'log' }, el('summary', { text: 'Module log' }), panel.pre),
    cards));
  return { id, mod, modEntry };
}

async function loadModules() {
  const outcomes = await Promise.all(MODULES.map(async ([id, load]) => {
    const t0 = performance.now();
    const outcome = await settle(Promise.resolve().then(load), IMPORT_TIMEOUT_MS);
    return { id, ms: Math.round(performance.now() - t0), outcome };
  }));
  return outcomes.map(({ id, ms, outcome }) => register(id, ms, outcome)).filter(Boolean);
}

async function resumeAll(loaded) {
  for (const { id, mod, modEntry } of loaded) {
    if (typeof mod.resume !== 'function') continue;
    const outcome = await settle(Promise.resolve().then(() => mod.resume(makeCtx(modEntry))), AUTO_TIMEOUT_MS);
    if (outcome.timedOut || outcome.failed) {
      const why = outcome.timedOut ? 'it did not finish within 30 s' : errText(outcome.error);
      state.modules[id].resumeError = why;
      modEntry.log(`resume failed: ${why}`);
      hlog(`${id}.resume failed: ${why}`);
      console.error(`Spike S1: ${id}.resume failed: ${why}`);
      continue;
    }
    const out = outcome.value;
    if (out == null) continue;
    if (typeof out !== 'object') {
      hlog(`${id}.resume returned ${asText(out)}, not an object`);
      continue;
    }
    for (const [cid, r] of Object.entries(out)) {
      const entry = state.byId.get(cid);
      if (!entry) {
        hlog(`${id}.resume reported an unknown check ${cid}`);
        continue;
      }
      entry.resumed = true;
      modEntry.log(`resumed ${cid}`);
      record(entry, normalise(r), typeof r?.ms === 'number' ? r.ms : null, 'resume');
    }
  }
}

// ---- rendering

function makeCard(entry) {
  const { check } = entry;
  const titleId = `t-${domId(check.id)}`;
  entry.ui = {
    pill: el('span', { class: 'pill' }),
    summary: el('p', { class: 'card-summary' }),
    ms: el('span', { class: 'ms' }),
    data: el('pre', { class: 'data' }),
    run: TAPPABLE.has(check.kind) ? el('button', { type: 'button', class: 'btn', onclick: () => tap(entry) }) : null,
  };
  entry.ui.card = el('article', { class: 'card', id: `check-${domId(check.id)}`, 'aria-labelledby': titleId },
    el('div', { class: 'card-head' }, el('h3', { class: 'card-title', id: titleId, text: check.title }), entry.ui.pill),
    typeof check.what === 'string' && check.what ? el('p', { class: 'what', text: check.what }) : null,
    el('div', { class: 'card-meta' }, el('span', { class: 'chip', 'data-kind': check.kind, text: KINDS[check.kind] }), el('code', { class: 'check-id', text: check.id }), entry.ui.ms),
    entry.ui.summary,
    entry.panel.prompts,
    entry.ui.run ? el('div', { class: 'actions' }, entry.ui.run) : null,
    entry.panel.mount,
    el('details', { class: 'log' }, el('summary', { text: 'Log and data' }), entry.panel.pre, entry.ui.data));
  paintCard(entry);
  return entry.ui.card;
}

function paintCard(entry) {
  const { ui: u, check, result } = entry;
  if (!u) return;
  const phase = entry.running ? (entry.asking ? 'asking' : 'running')
    : entry.queued ? 'queued'
      : result ? result.status
        : check.kind === 'republish' ? 'waiting' : 'pending';
  u.card.dataset.status = phase;
  u.pill.dataset.status = phase;
  u.pill.textContent = PILL[phase];
  u.summary.textContent = result ? result.summary : PENDING_TEXT[check.kind];
  u.ms.textContent = result && typeof result.ms === 'number' ? `${result.ms} ms` : '';
  u.data.textContent = entry.rawData === undefined ? '' : clip(JSON.stringify(entry.rawData, null, 1), 32_000);
  if (u.run) {
    const busy = entry.running || entry.queued;
    const blocked = check.kind === 'republish' && state.republish.phase !== 'arrived';
    u.run.disabled = busy || blocked;
    u.run.textContent = busy ? (entry.running ? 'Running' : 'Queued')
      : blocked ? 'Runs after the republish'
        : result ? 'Run again'
          : check.kind === 'consent' ? 'Run (may ask consent)' : 'Run';
  }
}

function tap(entry) {
  if (entry.running || entry.queued) return;
  if (entry.check.kind === 'republish' && state.republish.phase !== 'arrived') return;
  enqueue(entry, 'tap');
}

function paintSummary() {
  if (!ui.counts) return;
  const counts = Object.fromEntries(STATUSES.map(s => [s, 0]));
  let notRun = 0;
  for (const e of state.entries) {
    if (e.result) counts[e.result.status] += 1;
    else notRun += 1;
  }
  for (const r of Object.values(state.extraResults)) counts[r.status] += 1;
  ui.counts.replaceChildren(
    ...STATUSES.map(s => el('span', { class: 'count pill', 'data-status': s }, `${PILL[s]} ${counts[s]}`)),
    el('span', { class: 'count pill', 'data-status': 'pending' }, `${PILL.pending} ${notRun}`),
  );
  const autos = state.entries.filter(e => AUTO_KINDS.has(e.check.kind));
  const autosDone = autos.filter(e => e.result && !e.running && !e.queued).length;
  const finished = state.started && autosDone === autos.length;
  ui.progress.textContent = !state.started ? 'Loading the check modules.'
    : finished ? `Automatic checks finished: ${autos.length} of ${autos.length}.`
      : `Automatic checks: ${autosDone} of ${autos.length} done.`;
  if (finished && !state.autoFinished) {
    state.autoFinished = true;
    hlog('automatic checks finished');
    resolveAutoDone(true);
    paintRepublish();
  }
}

function paintHeader() {
  if (!ui.db) return;
  const w = state.writes;
  const failing = Object.keys(w.failing).length > 0;
  ui.db.dataset.state = state.dbState === 'connected' && failing ? 'failing' : state.dbState.replace(' ', '-');
  ui.db.textContent = state.dbState === 'connected'
    ? `connected, ${w.ok} saved${w.failed ? `, ${w.failed} failed` : ''}`
    : state.dbState === 'not available' ? 'not available' : 'connecting';
  const notes = [];
  if (state.lockError) notes.push(`lock.json did not load (${state.lockError}); checks that need it will say so.`);
  if (state.dbState === 'not available') notes.push('db is not available: results stay on this screen. Use Copy results to keep them.');
  if (failing && w.lastError) notes.push(`Last save failed: ${w.lastError}. Results stay on this screen and Copy results still works.`);
  const cut = state.truncatedIds.size;
  if (cut) notes.push(`Data of ${cut} ${cut === 1 ? 'check was' : 'checks were'} cut to fit the run document; see the harness log.`);
  ui.notice.replaceChildren(...notes.map(n => el('p', { text: n })));
  ui.notice.hidden = notes.length === 0;
}

function paintRepublish() {
  if (!ui.rp) return;
  const r = state.republish;
  const lines = []; // strings, and { quote } for the line the owner copies, kept beside its prompt
  if (r.phase === 'arrived') {
    const reps = state.entries.filter(e => e.check.kind === 'republish');
    const left = reps.filter(e => !e.result || e.running || e.queued || e.awaitingLate).length;
    lines.push(`The republish signal arrived at ${new Date(r.arrivedAt).toLocaleTimeString('en-GB')} (${r.source === 'manual' ? 'started by you' : `Claude wrote at ${asText(r.at)}`}).`);
    const late = reps.filter(e => e.awaitingLate).length;
    if (left) lines.push(`Running the republish checks: ${reps.length - left} of ${reps.length} done${late ? `, ${late} still finishing after a time limit` : ''}.`);
    else {
      lines.push('The republish checks finished. Tell Claude:');
      lines.push({ quote: 'S1 republish checks done' });
    }
  } else if (version !== 'v1') {
    lines.push(`This page is ${version}. The republish checks run on the v1 page that was kept open during the republish, so there is nothing to do here.`);
  } else if (!state.autoFinished) {
    lines.push('Step 1: wait here until the automatic checks finish.');
  } else {
    lines.push('Step 2: keep this page open and tell Claude:');
    lines.push({ quote: 'S1 ready for republish' });
    lines.push(state.dbState === 'not available'
      ? 'db is not available, so the signal cannot reach this page. When Claude says the republish is done, use the button below.'
      : 'This panel changes when Claude\'s signal (ops/s1-republished) arrives.');
  }
  if (r.stale && r.phase !== 'arrived') lines.push(`An older signal from before this page loaded (at ${asText(r.stale.at)}) was ignored.`);
  if (r.error) lines.push(`The signal watch reported: ${r.error}`);
  ui.rp.dataset.phase = r.phase;
  ui.rpText.replaceChildren(...lines.map(t => (typeof t === 'string' ? el('p', { text: t }) : el('p', { class: 'quote', text: t.quote }))));
  const manualOk = r.phase !== 'arrived' && version === 'v1' && state.autoFinished;
  ui.rpManual.hidden = !manualOk;
  if (!manualOk) ui.rpManual.dataset.armed = '';
  ui.rpManual.textContent = ui.rpManual.dataset.armed ? 'Tap again to confirm Claude has republished' : 'The signal did not arrive: start the republish checks';
}

function manualRepublish() {
  if (!ui.rpManual.dataset.armed) {
    ui.rpManual.dataset.armed = '1';
    paintRepublish();
    return;
  }
  hlog('republish checks started by hand');
  arrive({ at: new Date().toISOString(), to: 'v2', source: 'manual' });
}

// ---- copy results

function setCopyStatus(text) {
  ui.copyStatus.textContent = text;
}

function copyResults() {
  let json;
  try {
    json = buildRunDoc().json;
  } catch (e) {
    hlog(`could not build the results: ${errText(e)}`);
    setCopyStatus(`Could not build the results: ${errText(e)}`);
    return;
  }
  const kb = (bytesOf(json) / 1024).toFixed(1);
  const cb = navigator.clipboard;
  if (!cb || typeof cb.writeText !== 'function') return fallbackCopy(json, kb, 'the clipboard is not available here');
  let p;
  try {
    p = cb.writeText(json); // called inside the click handler, before any await
  } catch (e) {
    return fallbackCopy(json, kb, errText(e));
  }
  return p.then(
    () => {
      state.copy = { at: new Date().toISOString(), method: 'clipboard.writeText', kb: Number(kb) };
      setCopyStatus(`Copied ${kb} KB of results.`);
      hlog(`copied ${kb} KB of results`);
    },
    e => fallbackCopy(json, kb, errText(e)),
  );
}

function fallbackCopy(json, kb, reason) {
  hlog(`clipboard write failed: ${reason}`);
  if (!ui.copyArea) {
    ui.copyArea = el('textarea', { class: 'copy-area', readonly: true, rows: 8, 'aria-label': 'Results as JSON' });
    ui.copyBox.append(ui.copyArea);
  }
  const ta = ui.copyArea;
  ta.value = json;
  ta.hidden = false;
  ta.focus({ preventScroll: false });
  ta.select();
  try {
    ta.setSelectionRange(0, json.length);
  } catch (e) {
    hlog(`could not select the results: ${errText(e)}`);
  }
  let copied = false;
  try {
    copied = document.execCommand('copy');
  } catch (e) {
    hlog(`execCommand copy failed: ${errText(e)}`);
  }
  state.copy = { at: new Date().toISOString(), method: copied ? 'execCommand' : 'selected for the owner', writeTextError: clip(reason, 160), kb: Number(kb) };
  setCopyStatus(copied
    ? `Copied ${kb} KB of results with the fallback.`
    : `Copy was blocked (${reason}). The results are selected below: tap and hold, then Copy.`);
}

// ---- the shell

function saveAppVersion() {
  const v = ui.appInput.value.trim().slice(0, 80);
  const m = ui.modelInput.value.trim().slice(0, 80);
  state.appVersion = v;
  state.deviceModel = m;
  harnessSession.set('s1.appVersion', v || null);
  harnessSession.set('s1.deviceModel', m || null);
  const said = [v && `app ${v}`, m && `model ${m}`].filter(Boolean).join(', ');
  ui.appSaved.textContent = !said ? 'Cleared.' : state.dbState === 'connected' ? `Saved: ${said}` : `Kept on this screen: ${said}`;
  hlog(`Claude app version set to "${v}", iPhone model to "${m}"`);
  persist();
}

function renderShell() {
  ui.db = el('span', { class: 'db-state', 'data-state': 'connecting', text: 'connecting' });
  ui.notice = el('div', { class: 'notice', role: 'status', hidden: true });
  ui.appInput = el('input', {
    id: 's1-app-version', class: 'text-input', type: 'text', autocomplete: 'off', autocapitalize: 'off', spellcheck: 'false',
    placeholder: 'for example 1.250929.0', onkeydown: e => { if (e.key === 'Enter') saveAppVersion(); },
  });
  ui.appInput.value = harnessSession.get('s1.appVersion') ?? '';
  state.appVersion = ui.appInput.value;
  ui.modelInput = el('input', {
    id: 's1-device-model', class: 'text-input', type: 'text', autocomplete: 'off', autocapitalize: 'off', spellcheck: 'false',
    placeholder: 'for example iPhone 15 Pro', onkeydown: e => { if (e.key === 'Enter') saveAppVersion(); },
  });
  ui.modelInput.value = harnessSession.get('s1.deviceModel') ?? '';
  state.deviceModel = ui.modelInput.value;
  ui.appSaved = el('span', { class: 'saved', role: 'status' });
  ui.counts = el('div', { class: 'counts' });
  ui.progress = el('p', { class: 'progress', role: 'status' });
  ui.copyStatus = el('p', { class: 'copy-status', role: 'status' });
  ui.copyBox = el('div', { class: 'copy-box' });
  ui.rpText = el('div', { class: 'rp-text', role: 'status' });
  ui.rpManual = el('button', { type: 'button', class: 'btn', hidden: true, onclick: manualRepublish });
  ui.rp = el('section', { class: 'panel republish', 'aria-labelledby': 'rp-title' },
    el('h2', { class: 'panel-title', id: 'rp-title', text: 'Republish' }), ui.rpText, el('div', { class: 'actions' }, ui.rpManual));
  ui.harnessPre = el('pre', { class: 'log-lines' });
  for (const line of harnessLines) appendLine(ui.harnessPre, line);
  ui.modules = el('div', { class: 'modules' });

  app.replaceChildren(el('div', { class: 'shell' },
    el('header', { class: 'hdr' },
      el('h1', { class: 'hdr-title', text: 'Spike S1 Probe' }),
      el('dl', { class: 'meta' },
        el('div', {}, el('dt', { text: 'Page' }), el('dd', {}, el('span', { class: 'badge', 'data-version': version, text: version }))),
        el('div', {}, el('dt', { text: 'Run' }), el('dd', { class: 'mono', text: runId })),
        el('div', {}, el('dt', { text: 'db' }), el('dd', {}, ui.db))),
      ui.notice,
      el('div', { class: 'appver' },
        el('label', { for: 's1-app-version', text: 'Claude app version (from the app\'s settings)' }),
        ui.appInput,
        el('label', { for: 's1-device-model', text: 'iPhone model (Settings, General, About)' }),
        el('div', { class: 'appver-row' }, ui.modelInput, el('button', { type: 'button', class: 'btn', text: 'Save', onclick: saveAppVersion })),
        ui.appSaved)),
    el('div', { class: 'summary' }, ui.counts, ui.progress),
    el('div', { class: 'toolbar' },
      el('button', { type: 'button', class: 'btn btn-primary', text: 'Copy results', onclick: copyResults }),
      ui.copyStatus,
      ui.copyBox),
    ui.rp,
    el('details', { class: 'log harness-log' }, el('summary', { text: 'Harness log' }), ui.harnessPre),
    ui.modules));
  paintHeader();
  paintSummary();
  paintRepublish();
}

// ---- start

window.addEventListener('error', e => hlog(`page error: ${e.message ?? 'unknown'} at ${e.filename ?? '?'}:${e.lineno ?? '?'}`));
window.addEventListener('unhandledrejection', e => hlog(`unhandled rejection: ${errText(e.reason)}`));
document.addEventListener('visibilitychange', () => {
  hlog(`page is ${document.visibilityState}`);
  if (document.visibilityState === 'hidden' && state.db) flushFailed();
});
window.addEventListener('pageshow', e => hlog(`pageshow (from the back-forward cache: ${e.persisted})`));
window.addEventListener('pagehide', e => hlog(`pagehide (may be cached: ${e.persisted})`));

// A read-only handle for the local test run; the checks never use it.
window.__s1harness = Object.freeze({
  runId, version, autoDone,
  document: () => buildRunDoc().doc,
  limits: () => Object.fromEntries(state.entries.map(e => [e.id, limitOf(e.check)])),
});

async function main() {
  renderShell();
  hlog(`harness started: page ${version}, run ${runId}${previousRunId ? `, previous run ${previousRunId}` : ''}`);
  const dbReady = connectDb();
  await loadLock();
  const loaded = await loadModules();
  await resumeAll(loaded);
  state.started = true;
  for (const e of state.entries) if (AUTO_KINDS.has(e.check.kind) && !e.result) enqueue(e, 'auto');
  paintSummary();
  persist();
  await dbReady;
}

main().catch(e => {
  hlog(`harness fault: ${errText(e)}`);
  console.error('Spike S1: harness fault', e);
  if (ui.notice) {
    ui.notice.hidden = false;
    ui.notice.append(el('p', { text: `The harness stopped: ${errText(e)}` }));
  } else app.textContent = `The probe could not start: ${errText(e)}`;
});
