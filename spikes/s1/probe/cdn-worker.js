// Spike S1 probe: the module worker behind the check cdn.module-worker.
// Decision notes:
// - This file holds no URLs. The page posts the locked entry URLs, so cdn-lock.json stays the one source.
// - Libraries are imported and exercised one at a time, so a refusal or a slow closure is pinned to one library.
// - Inputs are fixed (a fixed date for ts-fsrs, a seeded 64 KB buffer for fflate), so results compare across devices.

const errText = (e) => {
  if (e == null) return String(e);
  const s = typeof e === 'object' && 'message' in e ? `${e.name || 'Error'}: ${e.message}` : String(e);
  return s.slice(0, 300);
};
const r1 = (v) => Math.round(v * 10) / 10;

const kindOf = (name) => {
  const n = String(name).toLowerCase();
  if (n.includes('fsrs')) return 'fsrs';
  if (n.includes('fflate')) return 'fflate';
  if (n.includes('zod')) return 'zod';
  return null;
};

const tests = {
  // Classic zod: one valid and one invalid object; method chaining shows the classic build, not mini.
  zod(mod) {
    const z = mod.z ?? mod.default ?? mod;
    const schema = z.object({ a: z.number() });
    const good = schema.safeParse({ a: 1 });
    const bad = schema.safeParse({ a: 'x' });
    const issue = bad.success ? null : (bad.error?.issues?.[0] ?? null);
    const result = {
      validSuccess: good.success,
      validA: good.success ? good.data.a : null,
      invalidSuccess: bad.success,
      invalidCode: issue?.code ?? null,
      invalidPath: Array.isArray(issue?.path) ? issue.path.map(String) : null,
      chaining: typeof z.string().optional === 'function',
    };
    const ok = good.success === true && good.data?.a === 1 && bad.success === false
      && result.invalidCode === 'invalid_type' && result.invalidPath?.[0] === 'a';
    return { ok, result };
  },

  // ts-fsrs: a new card on a fixed date, one repeat, the due offset for each of the four ratings.
  fsrs(mod, msg) {
    const now = new Date(msg.fsrsDate);
    const scheduler = mod.fsrs();
    const card = mod.createEmptyCard(now);
    const preview = scheduler.repeat(card, now);
    const R = mod.Rating;
    const ratings = [R.Again, R.Hard, R.Good, R.Easy];
    const dueMs = ratings.map((r) => +new Date(preview[r].card.due) - now.getTime());
    const result = {
      dueMs,
      scheduledDays: ratings.map((r) => preview[r].card.scheduled_days),
      states: ratings.map((r) => preview[r].card.state),
    };
    const ok = dueMs.every((v) => Number.isFinite(v) && v > 0)
      && dueMs.every((v, i) => i === 0 || v >= dueMs[i - 1]);
    return { ok, result };
  },

  // fflate: gzip then gunzip a deterministic 64 KB buffer (eight letters from an LCG), compare every byte.
  fflate(mod) {
    const n = 65536;
    const input = new Uint8Array(n);
    let x = 0x2545f491;
    for (let i = 0; i < n; i++) {
      x = (Math.imul(x, 1664525) + 1013904223) >>> 0;
      input[i] = 97 + (x >>> 29);
    }
    const gz = mod.gzipSync(input, { level: 6, mtime: 0 });
    const back = mod.gunzipSync(gz);
    const m = Math.min(n, back.length);
    let firstDiff = -1;
    for (let i = 0; i < m; i++) if (back[i] !== input[i]) { firstDiff = i; break; }
    if (firstDiff === -1 && back.length !== n) firstDiff = m;
    let fnv = 0x811c9dc5;
    for (let i = 0; i < gz.length; i++) fnv = Math.imul(fnv ^ gz[i], 0x01000193) >>> 0;
    const result = { inputBytes: n, gzipBytes: gz.length, gzipFnv: fnv.toString(16), outputBytes: back.length, firstDiff };
    return { ok: firstDiff === -1, result };
  },
};

self.onmessage = async (ev) => {
  const msg = ev.data;
  if (!msg || msg.k !== 'run' || !Array.isArray(msg.imports)) {
    self.postMessage({ k: 'bad-message', got: typeof msg });
    return;
  }
  for (const entry of msg.imports) {
    const name = String(entry?.name);
    const kind = kindOf(name);
    const rec = { k: 'lib', name, kind, ok: false, phase: 'import', importMs: null, runMs: null, error: null, result: null };
    let t = performance.now();
    let mod;
    try {
      mod = await import(entry.url);
      rec.importMs = r1(performance.now() - t);
    } catch (e) {
      rec.importMs = r1(performance.now() - t);
      rec.error = errText(e);
      self.postMessage(rec);
      continue;
    }
    rec.phase = 'run';
    t = performance.now();
    try {
      const out = kind ? tests[kind](mod, msg) : { ok: true, result: { exports: Object.keys(mod).length } };
      rec.ok = out.ok;
      rec.result = out.result;
      if (!out.ok) rec.error = 'the library ran but returned the wrong result';
    } catch (e) {
      rec.error = errText(e);
    }
    rec.runMs = r1(performance.now() - t);
    self.postMessage(rec);
  }
  self.postMessage({ k: 'done' });
};

self.postMessage({ k: 'ready', at: r1(performance.now()) });
