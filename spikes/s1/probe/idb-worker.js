// Spike S1 probe: IndexedDB inside a worker (docs/PLAN.md stage 2 item (c)), driven by platform.js.
//
// Decision notes:
// - No import or export, so the same file runs as a module worker (the check) and as a classic worker
//   (the comparison platform.js tries only when the module worker does not start).
// - Every step posts as it finishes, so a hang shows on the main thread as the last step reached.
// - The worker reports raw counts (puts that succeeded, records read, count(), mismatches); the main thread
//   decides pass or fail from them, not from a flag the worker sets.
// - The database is closed and deleted in `finally` whatever failed, and the result says whether the
//   deletion succeeded and whether indexedDB.databases() still lists it.
// - The ready message says whether this file runs as a module: top-level `this` is undefined in a module
//   and the global scope in a classic worker, so a browser that ignored { type: 'module' } is caught.

const IS_MODULE = this === undefined;
const DELETE_TIMEOUT_MS = 5000;
const r1 = v => Math.round(v * 10) / 10;
const errText = e => (e && typeof e === 'object' && 'message' in e ? `${e.name || 'Error'}: ${e.message}` : String(e)).slice(0, 300);
const post = m => self.postMessage(m);

// Deterministic records with strings, numbers, booleans, an array and a nested object.
const makeRecord = i => ({ id: i, text: `record ${i}`, n: i * 7 + 0.5, flags: [i % 2 === 0, i % 3 === 0], nested: { k: `k${i}`, list: [i, i + 1, i + 2] } });

function request(r) {
  return new Promise((resolve, reject) => {
    r.onsuccess = () => resolve(r.result);
    r.onerror = () => reject(r.error ?? new Error('the request failed'));
  });
}

function transactionDone(tx) {
  return new Promise((resolve, reject) => {
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error ?? new Error('the transaction failed'));
    tx.onabort = () => reject(tx.error ?? new Error('the transaction was aborted'));
  });
}

function openDb(name) {
  return new Promise((resolve, reject) => {
    let upgraded = false;
    const r = indexedDB.open(name, 1);
    r.onupgradeneeded = () => {
      upgraded = true;
      r.result.createObjectStore('records', { keyPath: 'id' });
    };
    r.onsuccess = () => resolve({ db: r.result, upgraded });
    r.onerror = () => reject(r.error ?? new Error('open failed'));
    r.onblocked = () => post({ type: 'step', step: 'open-blocked' });
  });
}

function deleteDb(name) {
  return new Promise(resolve => {
    const t0 = performance.now();
    let blocked = false;
    let done = false;
    const finish = out => {
      if (done) return;
      done = true;
      clearTimeout(timer);
      resolve({ ...out, blocked, ms: r1(performance.now() - t0) });
    };
    const timer = setTimeout(() => finish({ ok: false, error: `no answer in ${DELETE_TIMEOUT_MS / 1000} s` }), DELETE_TIMEOUT_MS);
    let r;
    try {
      r = indexedDB.deleteDatabase(name);
    } catch (e) {
      finish({ ok: false, error: `deleteDatabase threw ${errText(e)}` });
      return;
    }
    r.onsuccess = () => finish({ ok: true });
    r.onerror = () => finish({ ok: false, error: errText(r.error) });
    r.onblocked = () => { blocked = true; };
  });
}

async function run({ name, n }) {
  const out = { type: 'result', n, steps: [] };
  const step = s => {
    out.steps.push(s);
    post({ type: 'step', step: s });
  };
  if (typeof indexedDB === 'undefined' || !indexedDB) {
    out.error = 'indexedDB is not defined in this worker';
    return out;
  }
  const t0 = performance.now();
  let db = null;
  try {
    const opened = await openDb(name);
    db = opened.db;
    out.upgraded = opened.upgraded;
    out.openMs = r1(performance.now() - t0);
    step('opened');

    const records = Array.from({ length: n }, (_, i) => makeRecord(i));
    const tw = performance.now();
    const wtx = db.transaction('records', 'readwrite');
    const written = transactionDone(wtx);
    const store = wtx.objectStore('records');
    out.putOk = 0;
    for (const rec of records) store.put(rec).onsuccess = () => { out.putOk += 1; };
    await written;
    out.writeMs = r1(performance.now() - tw);
    step('written');

    const tr = performance.now();
    const rtx = db.transaction('records', 'readonly');
    const readDone = transactionDone(rtx);
    const rstore = rtx.objectStore('records');
    const [all, count] = await Promise.all([request(rstore.getAll()), request(rstore.count())]);
    await readDone;
    out.readMs = r1(performance.now() - tr);
    out.read = Array.isArray(all) ? all.length : null;
    out.count = count;
    out.mismatches = 0;
    out.firstMismatch = null;
    for (let i = 0; i < n; i++) {
      if (JSON.stringify(all[i]) !== JSON.stringify(records[i])) {
        out.mismatches += 1;
        if (out.firstMismatch === null) out.firstMismatch = i;
      }
    }
    step('read');
  } catch (e) {
    out.error = errText(e);
    out.failedAfter = out.steps.length ? out.steps[out.steps.length - 1] : 'start';
  } finally {
    if (db) {
      try {
        db.close();
      } catch (e) {
        out.closeError = errText(e);
      }
    }
    out.delete = await deleteDb(name);
    step('deleted');
    if (typeof indexedDB.databases === 'function') {
      try {
        const list = await indexedDB.databases();
        out.listedAfterDelete = list.some(d => d.name === name);
      } catch (e) {
        out.listedAfterDelete = null;
        out.databasesError = errText(e);
      }
    } else out.listedAfterDelete = null;
    out.totalMs = r1(performance.now() - t0);
  }
  return out;
}

self.onmessage = e => {
  const m = e.data;
  if (!m || m.cmd !== 'run') return;
  run(m).then(post, err => post({ type: 'result', n: m.n, steps: [], error: `the worker's run failed: ${errText(err)}` }));
};

post({ type: 'ready', hasIndexedDB: typeof indexedDB !== 'undefined' && !!indexedDB, module: IS_MODULE, ms: r1(performance.now()) });
