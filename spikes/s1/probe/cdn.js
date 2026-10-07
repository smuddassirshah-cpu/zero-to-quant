// Spike S1 probe, module 'cdn': third-party modules from the CDN through the page's import map
// (docs/PLAN.md stage 2 item (a); docs/ARCHITECTURE.md 6.2.7).
// Decision notes:
// - Every load is an import() or a <script> element. fetch() of a CDN URL is never used: the host's CSP forbids it.
// - An integrity verdict always has a control load of the same bytes, and a refusal counts only when the
//   bytes are shown to have arrived: the refused URL's Resource Timing entry has the file's size or status 200.
//   Where Resource Timing hides sizes (the control's entry is zero too), two wrong-hash URLs must both be
//   refused. A network or CSP failure therefore reads as inconclusive, never as enforcement. The import-map
//   verdict is kept in module state so the cdnjs check can say whether its loads prove identical bytes.
// - The import map is read back from the DOM by its id (s1-importmap) where a verdict depends on what it
//   lists, so another map the host puts first is not mistaken for ours, and a build defect (a missing or
//   correct hash in the "bad" entry) shows as inconclusive instead of a false fail. Every check that depends
//   on the map records how many maps the page has.
// - Resolution is checked, not assumed: a pass needs import.meta.resolve() of each bare specifier to give the
//   locked URL (or, where resolve is missing, a Resource Timing entry for the locked URL), so a map earlier in
//   the page that sends 'preact' elsewhere fails the check.
// - Resource Timing sizes can be zero in Safari; zero is reported as "not exposed", never as a measurement.
// - Expected worker values (ts-fsrs due offsets, fflate output) were computed in Node 22.22.0 from the same npm
//   files; a mismatch is recorded as evidence and named in the summary, it does not fail the loading check.

const CDN_HOSTS = ['cdn.jsdelivr.net', 'cdnjs.cloudflare.com'];
const FSRS_DATE = Date.UTC(2026, 9, 7);
const NODE_FSRS_DUE_MS = [60000, 360000, 600000, 691200000];
const NODE_FFLATE = { gzipBytes: 29088, gzipFnv: '2bcbfb2a' };
const UMD_GLOBALS = ['preact', 'preactHooks', 'preactSignalsCore', 'preactSignals'];
const MAP_ID = 's1-importmap';
const STATIC_SPECIFIERS = ['preact', 'preact/hooks', '@preact/signals', 'zod/mini'];
const state = { integrity: null };

const errText = (e) => {
  if (e == null) return String(e);
  const s = typeof e === 'object' && 'message' in e ? `${e.name || 'Error'}: ${e.message}` : String(e);
  return s.slice(0, 300);
};
const evText = (ev) => `${ev?.type ?? 'error'} event${ev?.message ? `: ${String(ev.message).slice(0, 200)}` : ev?.error ? `: ${errText(ev.error)}` : ', no message given'}`;
const r1 = (v) => Math.round(v * 10) / 10;
const kb = (b) => `${(b / 1024).toFixed(1)} KB`;
const fmtDur = (ms) => (ms < 3600000 ? `${r1(ms / 60000)} min` : ms < 86400000 ? `${r1(ms / 3600000)} h` : `${r1(ms / 86400000)} d`);

// A larger Resource Timing buffer, set when the harness imports this module, so the zod/mini closure (92 files)
// and later loads are not dropped at the default limit of 250 entries.
const timingBuffer = (() => {
  try {
    const entriesAtModuleLoad = performance.getEntriesByType('resource').length;
    performance.setResourceTimingBufferSize(1000);
    return { size: 1000, entriesAtModuleLoad };
  } catch (e) {
    return { size: null, error: errText(e) };
  }
})();

// Resolves {state: 'resolved', value} | {state: 'rejected', error} | {state: 'timeout'}; never rejects.
function settle(promise, ms) {
  return new Promise((resolve) => {
    const timer = setTimeout(() => resolve({ state: 'timeout' }), ms);
    Promise.resolve(promise).then(
      (value) => { clearTimeout(timer); resolve({ state: 'resolved', value }); },
      (error) => { clearTimeout(timer); resolve({ state: 'rejected', error }); },
    );
  });
}

async function timedImport(ctx, url, ms) {
  const t0 = ctx.now();
  const s = await settle(import(url), ms);
  return { ...s, ms: r1(ctx.now() - t0) };
}

const outcome = (s) => ({
  state: s.state,
  ms: s.ms,
  error: s.state === 'rejected' ? errText(s.error) : null,
  exports: s.state === 'resolved' && s.value ? Object.keys(s.value).length : null,
});

const hostOf = (url) => /^https?:\/\/([^/:?#]+)/i.exec(String(url))?.[1]?.toLowerCase() ?? null;

function packageOf(url) {
  const s = String(url);
  let m = /^https:\/\/cdn\.jsdelivr\.net\/npm\/((?:@[^/]+\/)?[^@/]+)@([^/]+)\//.exec(s);
  if (m) return `${m[1]}@${m[2]}`;
  m = /^https:\/\/cdnjs\.cloudflare\.com\/ajax\/libs\/([^/]+)\/([^/]+)\//.exec(s);
  if (m) return `cdnjs:${m[1]}@${m[2]}`;
  return 'other';
}

const cdnEntries = () => performance.getEntriesByType('resource').filter((e) => CDN_HOSTS.includes(hostOf(e.name)));
const entriesFor = (url) => performance.getEntriesByName(url, 'resource');
const lockModule = (ctx, specifier) => (ctx.lock?.modules ?? []).find((m) => m.specifier === specifier) ?? null;
const fileCount = (m) => (Array.isArray(m?.files) ? m.files.length : typeof m?.files === 'number' ? m.files : null);

// What this module's own resolution says: {supported, url} or {supported, url: null, error}.
function mapResolves(specifier) {
  if (typeof import.meta.resolve !== 'function') return { supported: false, url: null };
  try {
    return { supported: true, url: import.meta.resolve(specifier) };
  } catch (e) {
    return { supported: true, url: null, error: errText(e) };
  }
}

const mapCount = () => document.querySelectorAll('script[type="importmap"]').length;

// The page's own import map (by its id) as written in the DOM, or why it could not be read.
function readImportMap() {
  const count = mapCount();
  const el = document.getElementById(MAP_ID);
  if (!el) return { found: false, count, integrity: null };
  try {
    const j = JSON.parse(el.textContent);
    return { found: true, count, integrity: j && typeof j.integrity === 'object' ? j.integrity : {} };
  } catch (e) {
    return { found: true, count, integrity: null, error: errText(e) };
  }
}

// A sentence for summaries when the page has more than one import map, else ''.
const mapsNote = (count) => (count > 1 ? ` The page has ${count} import maps, so an earlier one may decide where a specifier goes.` : '');

// Resource Timing evidence for one URL: the first entries' sizes and status.
const timingOf = (url) => entriesFor(url).slice(0, 3).map((e) => ({
  ms: r1(e.duration), transferSize: e.transferSize ?? null, decodedBodySize: e.decodedBodySize ?? null, responseStatus: e.responseStatus ?? null,
}));
// True when an entry shows the file's bytes arrived (its size, or status 200 where the browser reports it).
const bytesArrived = (timing, bytes) => timing.some((t) => (bytes != null && t.decodedBodySize === bytes) || t.responseStatus === 200);
// True when Resource Timing exposes sizes for this host: the control load's entry has a non-zero size.
const sizesExposed = (timing) => timing.some((t) => t.decodedBodySize > 0);
// `exposed` says whether Resource Timing shows sizes here, so a zero reads as "hidden", not as a measurement.
const describeTiming = (timing, exposed) => (timing.length
  ? timing.map((t) => `${exposed || t.decodedBodySize > 0 ? `${t.decodedBodySize ?? 'no'} bytes` : 'size hidden'}, status ${t.responseStatus ?? 'not reported'}`).join('; ')
  : 'no Resource Timing entry');

// For each specifier: what import.meta.resolve() gives against the locked URL, or whether the locked URL loaded.
function resolutionCheck(resolved, expected) {
  const rows = {};
  const wrong = [];
  const unproven = [];
  for (const [spec, want] of Object.entries(expected)) {
    const got = resolved?.[spec] ?? { supported: false, url: null };
    const fetched = want ? entriesFor(want).length > 0 : false;
    rows[spec] = { lockUrl: want, resolvedUrl: got.url ?? null, resolveSupported: !!got.supported, lockUrlFetched: fetched, ...(got.error ? { error: got.error } : {}) };
    if (!want) unproven.push(`${spec} (lock.json has no URL for it)`);
    else if (got.supported && got.url !== want) wrong.push(`${spec} resolved to ${got.url ?? `nothing (${got.error ?? 'no error text'})`}, not ${want}`);
    else if (!got.supported && !fetched) unproven.push(`${spec} (no import.meta.resolve and no Resource Timing entry for the locked URL)`);
  }
  return { rows, wrong, unproven };
}

// JSON-safe copy of an object's primitive fields.
function flat(obj) {
  if (obj == null || typeof obj !== 'object') return { value: obj === undefined ? null : obj };
  const o = {};
  for (const [k, v] of Object.entries(obj)) {
    o[k] = v == null ? null : typeof v === 'string' ? v.slice(0, 300) : ['number', 'boolean'].includes(typeof v) ? v : `[${typeof v}]`;
  }
  return o;
}

const kindOf = (name) => {
  const n = String(name).toLowerCase();
  if (n.includes('fsrs')) return 'fsrs';
  if (n.includes('fflate')) return 'fflate';
  if (n.includes('zod')) return 'zod';
  return null;
};

// A valid SRI token that cannot match: the first base64 character of the digest is changed.
function mangle(integrity) {
  const m = /^(sha(?:256|384|512))-([A-Za-z0-9+/]+={0,2})$/.exec(String(integrity).trim());
  if (!m) return null;
  return `${m[1]}-${m[2][0] === 'A' ? 'B' : 'A'}${m[2].slice(1)}`;
}

// Inserts a classic script with SRI and CORS; resolves {outcome: 'load' | 'error' | 'timeout', ms, el}.
function loadScript(ctx, url, integrity, ms) {
  return new Promise((resolve) => {
    const el = document.createElement('script');
    const t0 = ctx.now();
    let timer = null;
    const done = (result, detail) => {
      clearTimeout(timer);
      el.onload = null;
      el.onerror = null;
      resolve({ outcome: result, ms: r1(ctx.now() - t0), detail: detail ?? null, el });
    };
    el.onload = () => done('load');
    el.onerror = (ev) => done('error', evText(ev));
    el.setAttribute('integrity', integrity);
    el.setAttribute('crossorigin', 'anonymous');
    el.src = url;
    timer = setTimeout(() => done('timeout'), ms);
    try {
      (document.head || document.documentElement).appendChild(el);
    } catch (e) {
      done('error', errText(e));
    }
  });
}

const checks = [
  {
    id: 'cdn.bootstrap-map',
    title: 'Import map honoured by the classic bootstrap',
    kind: 'auto',
    what: "Whether the fragment's classic bootstrap resolves import('preact') through the page's import map: it waits on the bootstrap's own record and needs a module that exports h.",
    async run(ctx) {
      const boot = ctx.boot;
      const data = {
        mapPresent: boot?.mapPresent ?? null,
        mapCountAtBoot: boot?.mapCount ?? null,
        mapCount: mapCount(),
        ms: null,
        error: null,
        lockUrl: lockModule(ctx, 'preact')?.url ?? null,
        moduleResolvesPreact: mapResolves('preact'),
      };
      const note = mapsNote(data.mapCount);
      if (!boot || typeof boot !== 'object' || !('preact' in boot)) {
        data.error = 'window.__s1boot has no preact record';
        return { status: 'error', summary: 'The bootstrap left no record of its import, so this check had nothing to read.', data };
      }
      const s = await settle(boot.preact, 20000);
      if (s.state === 'timeout') {
        return { status: 'inconclusive', summary: "The bootstrap's import('preact') had not settled after 20 s.", data };
      }
      if (s.state === 'rejected') {
        data.error = errText(s.error);
        return { status: 'fail', summary: `The bootstrap's import('preact') was rejected: ${data.error}`, data };
      }
      const rec = s.value;
      data.record = flat(rec);
      data.ms = typeof rec?.ms === 'number' ? r1(rec.ms) : null;
      data.error = rec?.error == null ? null : String(rec.error).slice(0, 300);
      if (rec?.ok !== true || rec?.hasH !== true) {
        const why = data.error ?? (rec?.ok === true ? 'the module has no h export' : 'no error text was recorded');
        return { status: 'fail', summary: `The bootstrap's import('preact') did not give Preact: ${why}.${note}`, data };
      }
      const took = data.ms == null ? '' : ` in ${data.ms} ms`;
      const res = data.moduleResolvesPreact;
      if (!data.lockUrl) {
        return { status: 'inconclusive', summary: `The bootstrap's import('preact') gave a module with h${took}, but lock.json gives no locked URL to compare its resolution with.${note}`, data };
      }
      if (res.supported) {
        if (res.url !== data.lockUrl) {
          return { status: 'fail', summary: `The bootstrap's import('preact') resolved, but not to the locked URL: 'preact' goes to ${res.url ?? `nothing (${res.error ?? 'no error text'})`}.${note}`, data };
        }
        return { status: 'pass', summary: `The bootstrap's import('preact') resolved through the map to the locked URL${took} and the module exports h.${note}`, data };
      }
      data.lockUrlFetched = entriesFor(data.lockUrl).length > 0;
      if (!data.lockUrlFetched) {
        return { status: 'inconclusive', summary: `The bootstrap's import('preact') gave a module with h${took}, but import.meta.resolve is missing and Resource Timing has no entry for the locked URL, so where 'preact' went is not shown.${note}`, data };
      }
      return { status: 'pass', summary: `The bootstrap's import('preact') gave a module with h${took}, and the locked URL was fetched (import.meta.resolve is missing here).${note}`, data };
    },
  },

  {
    id: 'cdn.static-import',
    title: 'Static bare imports through the map',
    kind: 'auto',
    what: 'Whether a module with static bare imports of preact, preact/hooks, @preact/signals and zod/mini loads through the map, renders, updates on a signal change and validates with zod/mini.',
    async run(ctx) {
      const t0 = ctx.now();
      const s = await settle(import('./cdn-static.js'), 20000);
      const importMs = r1(ctx.now() - t0);
      const data = { phases: { importMs }, error: null };
      if (s.state === 'timeout') {
        return { status: 'inconclusive', summary: 'The module with static bare imports had not loaded after 20 s.', data };
      }
      if (s.state === 'rejected') {
        data.error = errText(s.error);
        return { status: 'fail', summary: `The module with static bare imports of preact, preact/hooks, @preact/signals and zod/mini did not load: ${data.error}`, data };
      }
      if (typeof s.value?.run !== 'function') {
        data.error = 'cdn-static.js has no run export';
        return { status: 'error', summary: 'cdn-static.js loaded without its run function.', data };
      }
      const expected = Object.fromEntries(STATIC_SPECIFIERS.map((sp) => [sp, lockModule(ctx, sp)?.url ?? null]));
      const out = await s.value.run(ctx.mount, () => ctx.now(), Object.keys(expected));
      Object.assign(data.phases, out.phases);
      Object.assign(data, { render: out.render, update: out.update, zod: out.zod, parts: out.parts ?? null, error: out.error, mapCount: mapCount() });
      if (out.cleanupError) data.cleanupError = out.cleanupError;
      const res = resolutionCheck(out.resolved, expected);
      data.resolution = res.rows;
      const note = mapsNote(data.mapCount);
      if (out.ok && res.wrong.length) {
        return { status: 'fail', summary: `The module with static bare imports ran, but not on the locked files: ${res.wrong.join('; ')}.${note}`, data };
      }
      if (out.ok && res.unproven.length) {
        return { status: 'inconclusive', summary: `The module with static bare imports ran, but where these went is not shown: ${res.unproven.join('; ')}.${note}`, data };
      }
      if (out.ok) {
        return {
          status: 'pass',
          summary: `The static bare imports resolved through the map to the locked URLs and loaded in ${importMs} ms; Preact rendered, the component and the bound text both updated on the signal change (component after ${out.update.compMs} ms, both after ${data.phases.updateMs} ms), and zod/mini accepted the valid object and rejected the invalid one.${note}`,
          data,
        };
      }
      data.failedPhase = out.phase;
      const p = out.parts ?? {};
      const why = out.error
        ? `it threw during ${out.phase}: ${out.error}`
        : [
            !p.renderOk && 'the first render was wrong',
            !p.compOk && 'the component did not update on the signal change',
            !p.boundOk && 'the text bound to the signal did not update',
            !p.zodOk && 'zod/mini gave the wrong result',
          ].filter(Boolean).join('; ');
      return { status: 'fail', summary: `The module loaded in ${importMs} ms but ${why}.${note}`, data };
    },
  },

  {
    id: 'cdn.load-cost',
    title: 'Request count and sizes of the CDN modules',
    kind: 'auto',
    what: 'How many requests the CDN modules have cost so far, per package, and what Resource Timing reports for their duration and sizes.',
    async run(ctx) {
      const all = performance.getEntriesByType('resource');
      const cdn = all.filter((e) => CDN_HOSTS.includes(hostOf(e.name)));
      const byPackage = {};
      const tally = { protocols: {}, initiators: {}, hosts: {} };
      const bump = (o, k) => { o[k] = (o[k] ?? 0) + 1; };
      let durationSum = 0, transfer = 0, encoded = 0, decoded = 0, zeroSize = 0, zeroTransfer = 0, zeroEncoded = 0, zeroDecoded = 0;
      let first = Infinity, last = 0;
      for (const e of cdn) {
        const t = e.transferSize || 0, en = e.encodedBodySize || 0, de = e.decodedBodySize || 0;
        const p = (byPackage[packageOf(e.name)] ??= { count: 0, ms: 0, transfer: 0, encoded: 0, decoded: 0 });
        p.count += 1;
        p.ms += e.duration;
        p.transfer += t;
        p.encoded += en;
        p.decoded += de;
        durationSum += e.duration;
        transfer += t;
        encoded += en;
        decoded += de;
        if (!t && !en && !de) zeroSize += 1;
        if (!t) zeroTransfer += 1;
        if (!en) zeroEncoded += 1;
        if (!de) zeroDecoded += 1;
        first = Math.min(first, e.startTime);
        last = Math.max(last, e.responseEnd);
        bump(tally.protocols, e.nextHopProtocol || 'unreported');
        bump(tally.initiators, e.initiatorType || 'unreported');
        bump(tally.hosts, hostOf(e.name));
      }
      for (const p of Object.values(byPackage)) p.ms = r1(p.ms);
      const expectedFiles = Object.fromEntries((ctx.lock?.modules ?? []).map((m) => [m.specifier, fileCount(m)]));
      const data = {
        requests: cdn.length,
        hosts: tally.hosts,
        byPackage,
        expectedFiles,
        durationSumMs: r1(durationSum),
        spanMs: cdn.length ? r1(last - first) : 0,
        transferSize: transfer,
        encodedBodySize: encoded,
        decodedBodySize: decoded,
        zeroSizeEntries: zeroSize,
        zeroTransferEntries: zeroTransfer,
        zeroEncodedEntries: zeroEncoded,
        zeroDecodedEntries: zeroDecoded,
        protocols: tally.protocols,
        initiators: tally.initiators,
        allResourceEntries: all.length,
        timingBuffer,
      };
      if (!cdn.length) {
        return { status: 'info', summary: 'Resource Timing lists no CDN requests so far, so the load cost is not measured here.', data };
      }
      const top = Object.entries(byPackage).sort((a, b) => b[1].count - a[1].count).map(([k, v]) => `${k} ${v.count}`).join(', ');
      const zodNote = expectedFiles['zod/mini'] == null ? '' : ` (the zod/mini closure is ${expectedFiles['zod/mini']} files)`;
      // A field that is zero on every entry is "not exposed"; a partial zero count is named beside the sum.
      const field = (name, sum, zeros) => (zeros === cdn.length
        ? `${name} size not exposed (zero on every entry)`
        : `${name} ${kb(sum)}${zeros ? ` (${zeros} entries zero: cache, or not exposed)` : ''}`);
      const sizes = zeroSize === cdn.length
        ? 'the browser reported zero for every size field, so sizes were not measured'
        : [field('transfer', transfer, zeroTransfer), field('encoded', encoded, zeroEncoded), field('decoded', decoded, zeroDecoded)].join(', ');
      return {
        status: 'info',
        summary: `${cdn.length} CDN requests so far: ${top}${zodNote}; ${data.durationSumMs} ms of request time over a ${data.spanMs} ms span; ${sizes}.`,
        data,
      };
    },
  },

  {
    id: 'cdn.integrity-enforced',
    title: 'Import-map integrity enforced',
    kind: 'auto',
    what: "Whether the import map's integrity is enforced: a CDN file listed with a wrong hash must be refused after its bytes arrive (Resource Timing), while the same file at a URL with no integrity entry loads.",
    async run(ctx) {
      const bad = ctx.lock?.badIntegrity;
      const control = ctx.lock?.control;
      if (!bad?.url || !control?.url) {
        state.integrity = 'error';
        return { status: 'error', summary: 'lock.json has no badIntegrity or control entry, so the check had nothing to load.', data: { error: 'lock.badIntegrity or lock.control missing' } };
      }
      const second = bad.second?.url ? bad.second : null;
      const map = readImportMap();
      const note = mapsNote(map.count);
      const resolves = mapResolves('preact');
      const priorFetches = entriesFor(bad.url).length + (second ? entriesFor(second.url).length : 0);
      const knownGood = (ctx.lock.modules ?? []).find((m) => m.url === bad.url)?.integrity ?? null;
      const listed = map.integrity ? (map.integrity[bad.url] ?? null) : undefined;
      const listed2 = second && map.integrity ? (map.integrity[second.url] ?? null) : undefined;
      const b = await timedImport(ctx, bad.url, 12000);
      const b2 = second ? await timedImport(ctx, second.url, 12000) : null;
      const c = await timedImport(ctx, control.url, 12000);
      const timing = { bad: timingOf(bad.url), second: second ? timingOf(second.url) : [], control: timingOf(control.url) };
      const exposed = sizesExposed(timing.control);
      const arrived = bytesArrived(timing.bad, bad.bytes) || bytesArrived(timing.second, bad.bytes);
      const data = {
        badUrl: bad.url,
        badIntegrity: bad.integrity ?? null,
        fileBytes: bad.bytes ?? null,
        mapFound: map.found,
        mapCount: map.count,
        mapListsForBadUrl: listed === undefined ? `map not readable: ${map.found ? map.error : `no element with id ${MAP_ID}`}` : listed,
        mapListsForSecondUrl: second ? (listed2 === undefined ? 'map not readable' : listed2) : 'no second URL in lock.json',
        mapListsControl: map.integrity ? control.url in map.integrity : null,
        controlUrl: control.url,
        secondUrl: second?.url ?? null,
        priorFetchesOfBadUrls: priorFetches,
        moduleResolvesPreact: resolves,
        bad: outcome(b),
        second: b2 ? outcome(b2) : null,
        control: outcome(c),
        badUrlTiming: timing.bad,
        secondUrlTiming: timing.second,
        controlTiming: timing.control,
        sizesExposed: exposed,
        bytesArrivedAndRefused: arrived,
      };
      const result = (status, summary) => {
        state.integrity = status;
        return { status, summary: `${summary}${note}`, data };
      };
      if (resolves.supported && !resolves.url) {
        return result('inconclusive', "The import map is not in effect for this module (import.meta.resolve('preact') failed), so its integrity entries cannot apply.");
      }
      if (listed === null) {
        return result('inconclusive', map.count > 1
          ? `The page's own import map lists no integrity for the wrong-hash URL, and the page has ${map.count} import maps, so the test is void.`
          : 'The page\'s import map lists no integrity for the wrong-hash URL, so the test is void (a probe build defect).');
      }
      if (knownGood && (listed ?? bad.integrity) === knownGood) {
        return result('inconclusive', 'The "wrong" hash equals the file\'s real hash in lock.json, so the test is void (a probe build defect).');
      }
      const loadedBad = [b, b2].find((x) => x && x.state === 'resolved');
      if (loadedBad) {
        if (priorFetches > 0) {
          return result('inconclusive', 'A wrong-hash URL loaded, but it had been fetched before this check, so it may have come from the module map without an integrity check.');
        }
        return result('fail', `An import listed with a wrong integrity hash loaded in ${loadedBad.ms} ms, so import-map integrity is not enforced.`);
      }
      if (c.state !== 'resolved') {
        const why = c.state === 'timeout' ? 'it timed out' : data.control.error;
        return result('inconclusive', `The control (same file, no integrity entry) also failed (${why}), so the network or the CSP blocked both and enforcement is unknown.`);
      }
      if (b.state === 'timeout' || b2?.state === 'timeout') {
        return result('inconclusive', 'A wrong-hash import had not settled after 12 s, while the control loaded.');
      }
      if (arrived) {
        return result('pass', `The wrong-hash import was refused (${data.bad.error}) after its bytes arrived (${describeTiming([...timing.bad, ...timing.second], exposed)}), and the same file with no integrity entry loaded in ${c.ms} ms, so import-map integrity is enforced.`);
      }
      if (exposed) {
        return result('inconclusive', `The wrong-hash URL failed before its bytes arrived (${describeTiming([...timing.bad, ...timing.second], exposed)}), while Resource Timing shows the control's bytes, so the refusal may be a network failure, not integrity.`);
      }
      if (!b2) {
        return result('inconclusive', 'Resource Timing does not expose sizes for the CDN here and lock.json has no second wrong-hash URL, so one refusal cannot be told from a network failure.');
      }
      return result('pass', `Both wrong-hash URLs were refused (${data.bad.error}) and the same file with no integrity entry loaded in ${c.ms} ms. Resource Timing does not expose sizes for the CDN here, so the verdict rests on the two refusals beside the control.`);
    },
  },

  {
    id: 'cdn.cdnjs-candidates',
    title: 'cdnjs files identical to the npm files',
    kind: 'auto',
    what: "Which cdnjs URLs serve the npm file's bytes: each is imported with the npm file's hash in the map, so a load means identical bytes when map integrity is enforced.",
    async run(ctx) {
      const list = ctx.lock?.cdnjs;
      if (!Array.isArray(list)) {
        return { status: 'error', summary: 'lock.json has no cdnjs list, so nothing was tried.', data: { error: 'lock.cdnjs missing' } };
      }
      const integrityVerdict = state.integrity;
      if (!list.length) {
        return { status: 'info', summary: 'lock.json lists no cdnjs candidates, so nothing was tried.', data: { tried: 0, integrityVerdict } };
      }
      const map = readImportMap();
      const deadline = ctx.now() + 25000;
      const results = [];
      for (const c of list) {
        const left = deadline - ctx.now();
        const tail = String(c.url).replace(/^https:\/\/cdnjs\.cloudflare\.com\/ajax\/libs\//, '');
        const row = { specifier: String(c.specifier), label: `${c.specifier} (${tail})`, url: String(c.url), inMap: map.integrity ? map.integrity[c.url] === c.integrity : null };
        if (row.inMap === null) row.mapNote = 'map not readable';
        if (left < 1000) {
          results.push({ ...row, outcome: 'not tried', error: 'the 25 s budget was spent' });
          continue;
        }
        const before = cdnEntries().filter((e) => hostOf(e.name) === 'cdnjs.cloudflare.com').length;
        const o = await timedImport(ctx, c.url, Math.min(10000, left));
        const timing = entriesFor(c.url)[0];
        results.push({
          ...row,
          outcome: o.state === 'resolved' ? 'loaded' : o.state,
          ms: o.ms,
          error: o.state === 'rejected' ? errText(o.error) : null,
          newCdnjsRequests: cdnEntries().filter((e) => hostOf(e.name) === 'cdnjs.cloudflare.com').length - before,
          fetchedBytes: timing ? (timing.decodedBodySize ?? null) : null,
        });
        const last = results[results.length - 1];
        ctx.log(`${last.label}: ${last.outcome}${last.error ? ` (${last.error})` : ''}`);
      }
      const loaded = results.filter((r) => r.outcome === 'loaded');
      const proven = loaded.filter((r) => r.inMap === true);
      const unreadable = loaded.filter((r) => r.inMap === null);
      const missed = results.filter((r) => r.outcome !== 'loaded').map((r) => r.label);
      const data = { tried: results.length, integrityVerdict, mapCount: map.count, mapFound: map.found, results, comparedFile: 'the entry file only; files it imports from cdnjs carry no integrity entry' };
      const missedText = missed.length ? ` Not served or refused: ${missed.join(', ')}.` : '';
      const authority = ' Only each entry file is compared; the stage 4 lock tool remains the authority.';
      if (integrityVerdict === 'pass') {
        const unlisted = loaded.length - proven.length - unreadable.length;
        const unlistedText = unlisted ? ` ${unlisted} loaded without its hash in the map, so those prove nothing.` : '';
        const unreadableText = unreadable.length ? ` ${unreadable.length} loaded, but the page's map was not readable, so those prove nothing.` : '';
        return {
          status: 'info',
          summary: `cdnjs serves ${proven.length} of ${results.length} candidates byte-identical to npm: ${proven.map((r) => r.label).join(', ') || 'none'}.${missedText}${unlistedText}${unreadableText}${authority}${mapsNote(map.count)}`,
          data,
        };
      }
      const verdictText = integrityVerdict == null ? 'not measured in this run' : `"${integrityVerdict}"`;
      return {
        status: 'info',
        summary: `${loaded.length} of ${results.length} cdnjs URLs loaded: ${loaded.map((r) => r.label).join(', ') || 'none'}.${missedText} Import-map integrity was ${verdictText}, so a load here does not prove identical bytes.${authority}${mapsNote(map.count)}`,
        data,
      };
    },
  },

  {
    id: 'cdn.module-worker',
    title: 'Module worker importing by full URL',
    kind: 'auto',
    what: 'Whether a module worker can import classic zod, ts-fsrs and fflate from the CDN by full URL with import(), and run each on fixed inputs.',
    async run(ctx) {
      const imports = ctx.lock?.workerImports;
      if (!Array.isArray(imports) || !imports.length) {
        return { status: 'error', summary: 'lock.json has no workerImports, so the worker had nothing to import.', data: { error: 'lock.workerImports missing' } };
      }
      const missing = ['zod', 'fsrs', 'fflate'].filter((k) => !imports.some((e) => kindOf(e?.name) === k));
      // A worker has no import map and import() takes no integrity, so these imports are not hash-checked.
      const data = { startMs: null, totalMs: null, end: null, libs: {}, events: [], missing, error: null, integrityApplied: false };
      const t0 = ctx.now();
      let worker;
      try {
        worker = new Worker(new URL('./cdn-worker.js', import.meta.url), { type: 'module' });
      } catch (e) {
        data.error = errText(e);
        return { status: 'fail', summary: `The browser refused to create the module worker: ${data.error}`, data };
      }
      let started = false;
      data.end = await new Promise((resolve) => {
        const timer = setTimeout(() => resolve('timeout'), 25000);
        const finish = (why) => { clearTimeout(timer); resolve(why); };
        worker.onmessage = (ev) => {
          const m = ev.data;
          if (m?.k === 'ready') {
            started = true;
            data.startMs = r1(ctx.now() - t0);
            worker.postMessage({ k: 'run', imports: imports.map((e) => ({ name: String(e.name), url: String(e.url) })), fsrsDate: FSRS_DATE });
          } else if (m?.k === 'lib') {
            const { name, kind, ok, phase, importMs, runMs, error, result } = m;
            data.libs[name] = { kind, ok, phase, importMs, runMs, error, result };
            ctx.log(`${name}: ${ok ? `ok, import ${importMs} ms, run ${runMs} ms` : `failed at ${phase}: ${error}`}`);
          } else if (m?.k === 'done') {
            finish('done');
          } else {
            data.events.push(`unexpected message: ${String(m?.k)}`);
          }
        };
        worker.onerror = (ev) => {
          data.events.push(evText(ev));
          ev.preventDefault();
          if (!started) finish('error');
        };
        worker.onmessageerror = () => { data.events.push('messageerror event'); };
      });
      worker.terminate();
      data.totalMs = r1(ctx.now() - t0);

      const libs = Object.entries(data.libs).map(([name, l]) => ({ name, ...l }));
      const fs = libs.find((l) => l.kind === 'fsrs');
      if (fs?.ok) data.libs[fs.name].matchesNode = JSON.stringify(fs.result.dueMs) === JSON.stringify(NODE_FSRS_DUE_MS);
      const ff = libs.find((l) => l.kind === 'fflate');
      if (ff?.ok) data.libs[ff.name].matchesNode = ff.result.gzipBytes === NODE_FFLATE.gzipBytes && ff.result.gzipFnv === NODE_FFLATE.gzipFnv;

      if (!started) {
        const why = data.end === 'error' ? data.events[data.events.length - 1] : 'it sent nothing within 25 s';
        return { status: 'fail', summary: `The module worker did not start: ${why}.`, data };
      }
      const failed = libs.filter((l) => !l.ok);
      if (failed.length) {
        return { status: 'fail', summary: `In the module worker, ${failed.map((l) => `${l.name} failed at ${l.phase}: ${l.error}`).join('; ')}.`, data };
      }
      const pending = imports.map((e) => String(e.name)).filter((n) => !(n in data.libs));
      if (pending.length) {
        return { status: 'inconclusive', summary: `The module worker started but had not finished ${pending.join(', ')} after 25 s.`, data };
      }
      if (missing.length) {
        data.error = `lock.workerImports lacks ${missing.join(', ')}`;
        return { status: 'error', summary: `lock.json's workerImports lacks ${missing.join(', ')}, so the check is incomplete.`, data };
      }
      const mismatches = [fs, ff].filter((l) => l && data.libs[l.name].matchesNode === false).map((l) => l.name);
      const mismatchText = mismatches.length ? ` Output differs from Node's for ${mismatches.join(', ')} (see data).` : '';
      const due = fs ? ` ts-fsrs due offsets: ${fs.result.dueMs.map(fmtDur).join(', ')}.` : '';
      return {
        status: 'pass',
        summary: `A module worker started in ${data.startMs} ms, imported ${libs.map((l) => `${l.name} (${l.importMs} ms)`).join(', ')} by full URL and ran each.${due}${mismatchText} These imports are not hash-checked: a worker has no import map and import() takes no integrity.`,
        data,
      };
    },
  },

  {
    id: 'cdn.umd-fallback',
    title: 'Preact 10.29.8 UMD fallback with integrity',
    kind: 'auto',
    what: "Whether the named fallback works: Preact 10.29.8, its hooks, signals-core and @preact/signals load as classic CDN scripts with integrity, render with useState and update on a signal change; and the signals-core script with a wrong hash is refused while the same file with its correct hash loads.",
    async run(ctx) {
      const umd = ctx.lock?.umd;
      if (!Array.isArray(umd) || !umd.length) {
        return { status: 'error', summary: 'lock.json has no umd list, so nothing was loaded.', data: { error: 'lock.umd missing' } };
      }
      const label = (e) => `${e?.name ?? ''} ${e?.url ?? ''}`.toLowerCase();
      const preactE = umd.find((e) => label(e).includes('preact') && !label(e).includes('hooks') && !label(e).includes('signals'));
      const hooksE = umd.find((e) => label(e).includes('hooks'));
      const coreE = umd.find((e) => label(e).includes('signals-core'));
      const signalsE = umd.find((e) => label(e).includes('signals') && !label(e).includes('signals-core'));
      const badIntegrity = coreE ? mangle(coreE.integrity) : null;
      if (!preactE || !hooksE || !coreE || !signalsE || !badIntegrity) {
        const error = `lock.umd lacks ${[!preactE && 'the preact UMD', !hooksE && 'the hooks UMD', !coreE && 'the signals-core UMD', !signalsE && 'the signals UMD', coreE && !badIntegrity && 'a valid SHA hash on the signals-core UMD'].filter(Boolean).join(', ')}`;
        return { status: 'error', summary: `${error}, so the fallback could not be tried.`, data: { error } };
      }
      const pre = Object.fromEntries(UMD_GLOBALS.map((g) => [g, g in window]));
      const data = { preExisting: pre, preact: null, hooks: null, globals: null, rendered: null, bad: null, bad2: null, control: null, signals: null, signalRender: null, cleaned: null };
      if (UMD_GLOBALS.some((g) => pre[g])) {
        return { status: 'inconclusive', summary: `${UMD_GLOBALS.filter((g) => pre[g]).join(', ')} existed before this check, so the UMD globals cannot be attributed.`, data };
      }
      const deadline = ctx.now() + 25000;
      const budget = () => Math.max(1000, Math.min(8000, deadline - ctx.now()));
      const added = [];
      const rec = (r, url) => ({ url, outcome: r.outcome, ms: r.ms, detail: r.detail });
      const load = async (url, integrity) => {
        const r = await loadScript(ctx, url, integrity, budget());
        added.push(r.el);
        return r;
      };

      const p = await load(preactE.url, preactE.integrity);
      data.preact = rec(p, preactE.url);
      const hk = p.outcome === 'load' ? await load(hooksE.url, hooksE.integrity) : null;
      data.hooks = hk ? rec(hk, hooksE.url) : { url: hooksE.url, outcome: 'not tried', detail: 'the preact UMD did not load' };

      const P = window.preact;
      const H = window.preactHooks;
      data.globals = { preactH: typeof P?.h, preactRender: typeof P?.render, hooksUseState: typeof H?.useState };
      const ready = typeof P?.h === 'function' && typeof P?.render === 'function' && typeof H?.useState === 'function';
      if (ready) {
        const box = document.createElement('div');
        ctx.mount.appendChild(box);
        try {
          const Probe = () => {
            const [v] = H.useState('umd');
            return P.h('span', null, `${v} ok`);
          };
          P.render(P.h(Probe, null), box);
          data.rendered = box.textContent;
          P.render(null, box);
        } catch (e) {
          data.renderError = errText(e);
        }
        box.remove();
      }

      // The wrong-hash loads (two URLs), then the control: the same file with its correct hash.
      const b = await load(coreE.url, badIntegrity);
      const coreAfterBad = 'preactSignalsCore' in window;
      const b2 = await load(`${coreE.url}?s1-bad2`, badIntegrity);
      const coreAfterBad2 = 'preactSignalsCore' in window;
      const ctlUrl = `${coreE.url}?s1-control`;
      const ctl = await load(ctlUrl, coreE.integrity);
      const timing = { bad: timingOf(coreE.url), bad2: timingOf(`${coreE.url}?s1-bad2`), control: timingOf(ctlUrl) };
      data.bad = {
        url: coreE.url, listedIntegrity: coreE.integrity, usedIntegrity: badIntegrity, outcome: b.outcome, ms: b.ms, detail: b.detail,
        globalAppeared: coreAfterBad, fileBytes: coreE.bytes ?? null, timing: timing.bad,
      };
      data.bad2 = { url: `${coreE.url}?s1-bad2`, outcome: b2.outcome, ms: b2.ms, detail: b2.detail, globalAppeared: coreAfterBad2, timing: timing.bad2 };
      data.control = { ...rec(ctl, ctlUrl), definesGlobal: typeof window.preactSignalsCore?.signal === 'function', timing: timing.control };
      const exposed = sizesExposed(timing.control);
      const arrived = bytesArrived(timing.bad, coreE.bytes) || bytesArrived(timing.bad2, coreE.bytes);
      Object.assign(data, { sizesExposed: exposed, bytesArrivedAndRefused: arrived });

      // @preact/signals UMD on the control's signals-core, driving a Preact 10.29.8 render.
      if (ready && data.control.definesGlobal) {
        const sg = await load(signalsE.url, signalsE.integrity);
        data.signals = { ...rec(sg, signalsE.url), definesSignal: typeof window.preactSignals?.signal === 'function' };
        if (data.signals.definesSignal) {
          const box = document.createElement('div');
          ctx.mount.appendChild(box);
          try {
            const sig = window.preactSignals.signal(1);
            const Probe = () => {
              const [v] = H.useState('umd');
              return P.h('span', null, `${v} `, sig);
            };
            P.render(P.h(Probe, null), box);
            const first = box.textContent;
            sig.value = 2;
            const t0 = ctx.now();
            let updated = box.textContent === 'umd 2';
            while (!updated && ctx.now() - t0 < 2000) {
              await new Promise((resolve) => setTimeout(resolve, 10));
              updated = box.textContent === 'umd 2';
            }
            data.signalRender = { first, after: box.textContent, updated, ms: r1(ctx.now() - t0) };
            P.render(null, box);
          } catch (e) {
            data.signalRender = { error: errText(e) };
          }
          box.remove();
        }
      } else {
        data.signals = { url: signalsE.url, outcome: 'not tried', detail: ready ? 'the signals-core control did not define its global' : 'Preact 10.29.8 did not load' };
      }

      for (const el of added) el.remove();
      data.cleaned = {};
      for (const g of UMD_GLOBALS) if (!pre[g] && g in window) data.cleaned[g] = delete window[g];
      data.leftover = UMD_GLOBALS.filter((g) => !pre[g] && g in window);

      if ([b, b2].some((x) => x.outcome === 'load') || coreAfterBad || coreAfterBad2) {
        return { status: 'fail', summary: 'A classic script with a wrong integrity hash ran, so script integrity is not enforced.', data };
      }
      const goodFail = [[p, 'preact'], [hk, 'hooks']].find(([r]) => r && r.outcome !== 'load');
      if (goodFail) {
        const [r, which] = goodFail;
        if (r.outcome === 'timeout') return { status: 'inconclusive', summary: `The ${which} UMD neither loaded nor failed within its time limit.`, data };
        return { status: 'fail', summary: `The ${which} UMD with its correct integrity was refused (${r.detail}).`, data };
      }
      if (data.rendered !== 'umd ok') {
        const why = data.renderError ?? `globals were h ${data.globals.preactH}, render ${data.globals.preactRender}, useState ${data.globals.hooksUseState}; rendered ${JSON.stringify(data.rendered)}`;
        return { status: 'fail', summary: `The UMD scripts loaded but did not render: ${why}.`, data };
      }
      if (ctl.outcome !== 'load' || !data.control.definesGlobal) {
        return { status: 'inconclusive', summary: `The signals-core script with its correct hash did not load (${ctl.outcome}${ctl.detail ? `: ${ctl.detail}` : ''}), so the wrong-hash refusals cannot be told from a network failure, and the signals UMD was not tried.`, data };
      }
      if (b.outcome === 'timeout' || b2.outcome === 'timeout') {
        return { status: 'inconclusive', summary: 'Preact 10.29.8 rendered from the UMD scripts, but a wrong-hash script neither loaded nor failed in time.', data };
      }
      if (!arrived && exposed) {
        return { status: 'inconclusive', summary: `The wrong-hash script failed before its bytes arrived (${describeTiming([...timing.bad, ...timing.bad2], exposed)}), while Resource Timing shows the control's bytes, so the refusal may be a network failure, not integrity.`, data };
      }
      if (data.signals?.outcome !== 'load' || !data.signals.definesSignal) {
        return { status: 'fail', summary: `The @preact/signals UMD with its correct hash did not load or define its global (${data.signals?.outcome ?? 'not tried'}${data.signals?.detail ? `: ${data.signals.detail}` : ''}).`, data };
      }
      if (!data.signalRender?.updated) {
        return { status: 'fail', summary: `The @preact/signals UMD loaded, but a signal did not drive the Preact 10.29.8 render: ${data.signalRender?.error ?? `the text went from ${JSON.stringify(data.signalRender?.first)} to ${JSON.stringify(data.signalRender?.after)}`}.`, data };
      }
      const refusal = arrived
        ? `the signals-core script with a wrong hash was refused after its bytes arrived (${describeTiming(timing.bad, exposed)})`
        : 'the signals-core script with a wrong hash was refused at two URLs (Resource Timing does not expose sizes here)';
      return {
        status: 'pass',
        summary: `Preact 10.29.8, its hooks, signals-core and @preact/signals loaded as classic scripts with integrity, rendered with useState and updated on a signal change in ${data.signalRender.ms} ms; ${refusal}, while the same file with its correct hash loaded in ${ctl.ms} ms.`,
        data,
      };
    },
  },
];

export default { id: 'cdn', title: 'CDN modules and the import map', checks };
