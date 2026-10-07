// Spike S1 build: writes dist/v1/, dist/v2/, dist/v3/ and dist/dbsize/ from our own sources and cdn-lock.json.
//
// Decision notes:
// - Every integrity value the page carries is recomputed here from the unpacked npm tarballs and compared
//   with cdn-lock.json; a mismatch stops the build. The import closure is then walked again from the map's
//   imports (static specifiers from Node's own module parser, dynamic import() calls from a comment- and
//   string-aware scan), and any reached URL without an integrity entry, or a non-literal import(), stops the
//   build. The scan skips regular-expression literals heuristically, so a dynamic import hidden after one
//   could be missed [our estimate: none in today's closure, which a reviewer also walked by hand].
// - The bad-integrity probe reuses the jsx-runtime entry URL: an import map holds one integrity per URL,
//   so that URL carries the wrong hash and lock.json says so in the module's note. A second wrong-hash URL
//   (the same file with ?s1-bad2) backs the verdict where Resource Timing hides sizes. The control is the
//   same file at a URL with a query string and no integrity entry.
// - The import map carries id="s1-importmap", so the probe reads its own map even when the host puts
//   another map first.
// - The output is deterministic (no clock, no randomness), so dist/manifest.json doubles as a SHA-256
//   ledger and the publish plan Claude follows (CONTRACT.md, the runbook): the v2 diff, its planned size
//   and a two-batch split in case null removals count against the 255 paths of one publish.
// - The capability declarations are written once here, into lock.json (so the page records what it was
//   meant to be published with) and into the manifest (for the publishing session).
// - Missing sources written by other builders are reported, not fatal; pass --strict to make them fatal.
//   A present JavaScript file that does not parse is always fatal.

import { createHash } from 'node:crypto';
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DIST = path.join(ROOT, 'dist');
const STRICT = process.argv.includes('--strict');
const ALLOWED_EXT = new Set(['.html', '.js', '.mjs', '.css', '.json', '.svg']);
const MAX_FILE_BYTES = 1024 * 1024;
const MAX_PATHS = 255; // the most files one publish may send [sourced: the Artifact tool's description]

const PAGE_SPECIFIERS = ['preact', 'preact/hooks', 'preact/jsx-runtime', '@preact/signals', '@preact/signals-core', 'zod/mini', 'katex', 'ts-fsrs', 'fflate'];
const BAD_SPECIFIER = 'preact/jsx-runtime';
const MAP_ID = 's1-importmap';
const EXPECTED_PROBE = ['harness.js', 'cdn.js', 'cdn-static.js', 'cdn-worker.js', 'mathml.js', 'specimen.js', 'platform.js', 'idb-worker.js', 'locks-worker.js', 'caps.js', 'style.css'];
const CDNJS = 'https://cdnjs.cloudflare.com/ajax/libs';
// cdnjs paths are guesses at its layout [unverified]; a 404 only means "not served there". The stage 4 lock
// tool, not this probe, decides which cdnjs files the app may use.
const CDNJS_CANDIDATES = [
  ['preact', `${CDNJS}/preact/11.0.0/preact.mjs`],
  ['preact', `${CDNJS}/preact/11.0.0/dist/preact.mjs`],
  ['preact/hooks', `${CDNJS}/preact/11.0.0/hooks.mjs`],
  ['preact/hooks', `${CDNJS}/preact/11.0.0/hooks/dist/hooks.mjs`],
  ['@preact/signals', `${CDNJS}/preact-signals/2.11.3/signals.mjs`],
  ['@preact/signals', `${CDNJS}/preact-signals/2.11.3/dist/signals.mjs`],
  ['@preact/signals-core', `${CDNJS}/preact-signals-core/1.14.4/signals-core.mjs`],
  ['@preact/signals-core', `${CDNJS}/preact-signals-core/1.14.4/dist/signals-core.mjs`],
  ['zod/mini', `${CDNJS}/zod/4.6.5/mini/index.js`],
  ['zod/mini', `${CDNJS}/zod/4.6.5/mini/index.mjs`],
  ['katex', `${CDNJS}/KaTeX/0.19.0/katex.mjs`],
  ['katex', `${CDNJS}/KaTeX/0.19.0/dist/katex.mjs`],
  ['fflate', `${CDNJS}/fflate/0.8.3/esm/browser.js`],
  ['fflate', `${CDNJS}/fflate/0.8.3/browser.js`],
];
// UMD files for the no-import-map fallback, in load order, with the global each one defines.
const UMD = [
  { name: 'preact', global: 'preact', npmDir: 'npm/preact-10.29.8/package', path: 'dist/preact.umd.js', url: 'https://cdn.jsdelivr.net/npm/preact@10.29.8/dist/preact.umd.js' },
  { name: 'preact/hooks', global: 'preactHooks', npmDir: 'npm/preact-10.29.8/package', path: 'hooks/dist/hooks.umd.js', url: 'https://cdn.jsdelivr.net/npm/preact@10.29.8/hooks/dist/hooks.umd.js' },
  { name: '@preact/signals-core', global: 'preactSignalsCore', npmDir: 'npm/preact-signals-core-1.14.4/package', path: 'dist/signals-core.min.js', url: 'https://cdn.jsdelivr.net/npm/@preact/signals-core@1.14.4/dist/signals-core.min.js' },
  { name: '@preact/signals', global: 'preactSignals', npmDir: 'npm/preact-signals-2.11.3/package', path: 'dist/signals.min.js', url: 'https://cdn.jsdelivr.net/npm/@preact/signals@2.11.3/dist/signals.min.js' },
];
const WORKER_IMPORTS = [
  { name: 'zod', specifier: 'zod', url: 'https://cdn.jsdelivr.net/npm/zod@4.6.5/index.js' },
  { name: 'ts-fsrs', specifier: 'ts-fsrs', url: 'https://cdn.jsdelivr.net/npm/ts-fsrs@5.4.2/dist/index.mjs' },
  { name: 'fflate', specifier: 'fflate', url: 'https://cdn.jsdelivr.net/npm/fflate@0.8.3/esm/browser.js' },
];
// The probe's declaration: ARCHITECTURE.md 6.2.4's rule set unchanged, plus one canary rule that only a
// declared rule set can produce (caps.db-rules): with no rule at the s1canary prefix, siblings' subtrees stay
// private, the owner included [sourced: db.d.ts], so the owner's write to s1canary/zz-not-me must be refused.
// The publishing session checks the declaration against the artifact-capabilities skill before publishing.
const PROBE_CAPABILITIES = {
  db: { rules: [
    { path: '', read: 'interact', write: 'owner' },
    { path: 'data/users/{self}', write: 'interact' },
    { path: 'board', read: 'interact', write: 'owner' },
    { path: 'board/{self}', write: 'interact' },
    { path: 'meta', read: 'view', write: 'owner' },
    { path: 's1canary/{self}', write: 'interact' },
  ] },
  user: { scopes: ['profile'] },
  sample: {},
};
const DBSIZE_CAPABILITIES = { db: {} };

const warnings = [];
const fail = msg => { console.error(`build: ${msg}`); process.exit(1); };
const warn = msg => { warnings.push(msg); console.warn(`build: warning: ${msg}`); };
const sha384 = buf => `sha384-${createHash('sha384').update(buf).digest('base64')}`;
const sha256 = buf => createHash('sha256').update(buf).digest('hex');
const rel = p => path.relative(ROOT, p);

function npmFile(npmDir, file) {
  const p = path.join(ROOT, npmDir, file);
  if (!fs.existsSync(p)) fail(`npm file missing: ${rel(p)}`);
  return fs.readFileSync(p);
}

// ---- the lock: recompute every hash from npm/ and compare with cdn-lock.json

const cdnLock = JSON.parse(fs.readFileSync(path.join(ROOT, 'cdn-lock.json'), 'utf8'));
const bySpecifier = new Map(cdnLock.modules.map(m => [m.specifier, m]));
const verified = new Map(); // url -> integrity recomputed from npm
const sourceOf = new Map(); // url -> absolute npm path, for the closure walk

function verifyModule(spec) {
  const m = bySpecifier.get(spec);
  if (!m) fail(`cdn-lock.json has no module for ${spec}`);
  let bytes = 0;
  for (const f of m.files) {
    const buf = npmFile(m.npmDir, f.path);
    const got = sha384(buf);
    if (got !== f.integrity) fail(`integrity mismatch for ${f.url}: lock ${f.integrity}, npm ${got}`);
    if (buf.length !== f.bytes) fail(`size mismatch for ${f.url}: lock ${f.bytes}, npm ${buf.length}`);
    verified.set(f.url, got);
    sourceOf.set(f.url, path.join(ROOT, m.npmDir, f.path));
    bytes += buf.length;
  }
  const entry = m.files.find(f => f.url === m.url);
  if (!entry) fail(`entry ${m.url} of ${spec} is not in its own closure`);
  return { m, entry, bytes };
}

const pageModules = PAGE_SPECIFIERS.map(verifyModule);
const lockModules = pageModules.map(({ m, entry, bytes }) => ({
  specifier: m.specifier,
  url: m.url,
  integrity: entry.integrity,
  files: m.files.length,
  bytes,
  entryBytes: entry.bytes,
  ...(m.specifier === BAD_SPECIFIER
    ? { note: 'The import map lists this URL with the deliberately wrong hash of badIntegrity, so importing this specifier fails wherever import map integrity is enforced.' }
    : {}),
}));

const badModule = pageModules.find(p => p.m.specifier === BAD_SPECIFIER);
const badHash = sha384(Buffer.from('Spike S1: a deliberately wrong integrity value'));
const badHash2 = sha384(Buffer.from('Spike S1: a second deliberately wrong integrity value'));
if (badHash === verified.get(badModule.m.url) || badHash2 === verified.get(badModule.m.url)) fail('a wrong hash equals the real one');
const badIntegrity = {
  specifier: BAD_SPECIFIER,
  url: badModule.m.url,
  integrity: badHash,
  bytes: badModule.entry.bytes,
  second: { url: `${badModule.m.url}?s1-bad2`, integrity: badHash2 },
};
const control = { specifier: BAD_SPECIFIER, url: `${badModule.m.url}?s1-control` };

const cdnjs = CDNJS_CANDIDATES.map(([specifier, url]) => {
  const { m } = pageModules.find(p => p.m.specifier === specifier);
  return { specifier, url, integrity: sha384(npmFile(m.npmDir, m.entry)), replaces: m.url };
});

const lockUmd = UMD.map(u => {
  const buf = npmFile(u.npmDir, u.path);
  const integrity = sha384(buf);
  const listed = cdnLock.umd.find(x => x.url === u.url);
  if (listed && listed.integrity !== integrity) fail(`UMD integrity mismatch for ${u.url}`);
  return { name: u.name, global: u.global, url: u.url, integrity, bytes: buf.length };
});

const workerImports = WORKER_IMPORTS.map(w => {
  const { m, entry, bytes } = verifyModule(w.specifier);
  if (m.url !== w.url) fail(`worker import ${w.name}: lock entry ${m.url} differs from ${w.url}`);
  return { name: w.name, url: w.url, integrity: entry.integrity, files: m.files.length, bytes };
});

const lock = {
  note: 'Generated by tools/build.mjs from cdn-lock.json; every hash was recomputed from the npm tarballs.',
  modules: lockModules,
  umd: lockUmd,
  cdnjs,
  badIntegrity,
  control,
  workerImports,
  capabilities: PROBE_CAPABILITIES,
};

// ---- the import map

const integrity = {};
for (const { m } of pageModules) for (const f of m.files) integrity[f.url] = f.integrity;
for (const c of cdnjs) integrity[c.url] = c.integrity;
integrity[badIntegrity.url] = badIntegrity.integrity; // overrides the real hash on purpose
integrity[badIntegrity.second.url] = badIntegrity.second.integrity;
const importMap = { imports: Object.fromEntries(pageModules.map(({ m }) => [m.specifier, m.url])), integrity };

// ---- the closure walk: every URL the map's imports reach must carry an integrity entry

// Positions of import( outside comments, strings and template text; regular expressions are not tracked.
function dynamicImportArgs(src) {
  const out = [];
  const n = src.length;
  const skipQuoted = (i, q) => {
    for (let j = i + 1; j < n; j++) {
      if (src[j] === '\\') j++;
      else if (src[j] === q || (src[j] === '\n' && q !== '`')) return j + 1;
    }
    return n;
  };
  // Scans code from i; returns the index after the matching close brace when `inBraces`, else n.
  const scan = (i, inBraces) => {
    let depth = 0;
    while (i < n) {
      const c = src[i];
      if (c === '/' && src[i + 1] === '/') { const j = src.indexOf('\n', i); i = j < 0 ? n : j; continue; }
      if (c === '/' && src[i + 1] === '*') { const j = src.indexOf('*/', i + 2); i = j < 0 ? n : j + 2; continue; }
      if (c === '"' || c === "'") { i = skipQuoted(i, c); continue; }
      if (c === '`') { i = template(i + 1); continue; }
      if (inBraces && c === '{') depth++;
      if (inBraces && c === '}') { if (depth === 0) return i + 1; depth--; }
      if (c === 'i' && src.startsWith('import', i) && !/[\w$.]/.test(src[i - 1] ?? '') && !/[\w$]/.test(src[i + 6] ?? '')) {
        let j = i + 6;
        while (j < n && /\s/.test(src[j])) j++;
        if (src[j] === '(') out.push(src.slice(j + 1, j + 121));
        i = j;
        continue;
      }
      i++;
    }
    return n;
  };
  const template = i => {
    while (i < n) {
      if (src[i] === '\\') i += 2;
      else if (src[i] === '`') return i + 1;
      else if (src[i] === '$' && src[i + 1] === '{') i = scan(i + 2, true);
      else i++;
    }
    return n;
  };
  scan(0, false);
  return out;
}

function closureProblems() {
  const urls = [...sourceOf.keys()];
  const script = `const vm = require('node:vm'); const fs = require('node:fs');
const out = {};
for (const [url, file] of JSON.parse(process.argv[1])) {
  try { out[url] = { deps: new vm.SourceTextModule(fs.readFileSync(file, 'utf8'), { identifier: url }).dependencySpecifiers }; }
  catch (e) { out[url] = { error: String(e && e.message || e) }; }
}
process.stdout.write(JSON.stringify(out));`;
  const r = spawnSync(process.execPath, ['--experimental-vm-modules', '--no-warnings', '-e', script, JSON.stringify(urls.map(u => [u, sourceOf.get(u)]))], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
  if (r.status !== 0) return [`closure walk: the module parser failed: ${(r.stderr || '').trim().split('\n')[0]}`];
  const parsed = JSON.parse(r.stdout);
  const found = [];
  const reached = new Set();
  const queue = [...new Set(Object.values(importMap.imports))];
  const resolve = (spec, from) => {
    if (/^(\.{0,2}\/)/.test(spec)) return new URL(spec, from).href;
    if (/^https?:\/\//.test(spec)) return spec;
    return importMap.imports[spec] ?? null;
  };
  while (queue.length) {
    const url = queue.shift();
    if (reached.has(url)) continue;
    reached.add(url);
    const base = url.split('?')[0];
    if (!integrity[url]) found.push(`closure walk: ${url} is reached but has no integrity entry`);
    const info = parsed[base];
    if (!info) { found.push(`closure walk: ${url} is reached but its source is not in cdn-lock.json, so it cannot be scanned`); continue; }
    if (info.error) { found.push(`closure walk: ${base} does not parse as a module: ${info.error}`); continue; }
    const deps = [...info.deps];
    for (const arg of dynamicImportArgs(fs.readFileSync(sourceOf.get(base), 'utf8'))) {
      const lit = /^\s*(["'])([^"'\n]+)\1\s*\)/.exec(arg);
      if (lit) deps.push(lit[2]);
      else found.push(`closure walk: ${base} has a non-literal import(${arg.slice(0, 40)}`);
    }
    for (const spec of deps) {
      const next = resolve(spec, base);
      if (next === null) found.push(`closure walk: ${base} imports the bare specifier ${spec}, which the map does not resolve`);
      else if (!reached.has(next)) queue.push(next);
    }
  }
  return { problems: found, reached: reached.size };
}

// ---- the fragment

const FONTS = 'https://fonts.googleapis.com/css2?family=Archivo:wght@400..700&family=Source+Code+Pro:wght@400;600&display=swap';
const BOOTSTRAP = `(function () {
  var boot = window.__s1boot = {
    start: performance.now(),
    mapPresent: !!document.getElementById('${MAP_ID}'),
    mapCount: document.querySelectorAll('script[type=importmap]').length
  };
  boot.preact = import('preact').then(
    function (m) { return { ok: true, ms: performance.now() - boot.start, hasH: typeof m.h === 'function' }; },
    function (e) { return { ok: false, ms: performance.now() - boot.start, error: String(e) }; }
  );
  import('./harness.js').catch(function (e) {
    var app = document.getElementById('app');
    if (app) app.textContent = 'The probe could not start: ' + String(e);
    console.error('The probe could not start:', e);
  });
})();`;

try {
  new vm.Script(BOOTSTRAP, { filename: 'bootstrap.js' }); // parse only, never run
} catch (e) {
  fail(`the bootstrap script does not parse: ${e.message}`);
}

const BOOT_LINE = 'The probe is loading. If this line is still here after a minute, the page\'s scripts did not run: tell Claude.';
const fragment = version => [
  '<title>Spike S1 Probe</title>',
  '<link rel="preconnect" href="https://fonts.googleapis.com">',
  '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
  `<link rel="stylesheet" href="${FONTS.replaceAll('&', '&amp;')}">`,
  '<link rel="stylesheet" href="./style.css">',
  `<div id="app" data-version="${version}"><p class="boot-line">${BOOT_LINE}</p></div>`,
  `<script type="importmap" id="${MAP_ID}">${JSON.stringify(importMap, null, 1)}</script>`,
  `<script>\n${BOOTSTRAP}\n</script>`,
  '',
].join('\n');

// ---- data files

// About 64 KB of repetitive JSON: far above any compression threshold, small enough to read before publishing.
function compressJson() {
  const kinds = ['probability', 'statistics', 'linear-algebra', 'calculus', 'markets', 'programming'];
  const records = [];
  let size = 0;
  for (let i = 0; size < 64_000; i++) {
    const r = {
      id: i,
      slug: `item-${String(i).padStart(5, '0')}`,
      kind: kinds[i % kinds.length],
      level: (i % 7) + 1,
      score: ((i * 37) % 1000) / 10,
      done: i % 3 === 0,
      tags: [kinds[(i + 1) % kinds.length], kinds[(i + 2) % kinds.length]],
      note: 'Deterministic record for the compression probe.',
    };
    size += JSON.stringify(r).length + 1;
    records.push(r);
  }
  return JSON.stringify({ name: 'compress', note: 'Deterministic, compressible test data. Identical in v1 and v2.', count: records.length, records });
}

// ---- write

fs.rmSync(DIST, { recursive: true, force: true });
const written = new Map(); // folder -> [{ path, abs }]

function put(folder, file, content) {
  const abs = path.join(DIST, folder, file);
  fs.mkdirSync(path.dirname(abs), { recursive: true });
  fs.writeFileSync(abs, content);
  if (!written.has(folder)) written.set(folder, []);
  written.get(folder).push({ path: file, abs });
}

const probeDir = path.join(ROOT, 'probe');
const probeFiles = fs.existsSync(probeDir) ? fs.readdirSync(probeDir).filter(f => f.endsWith('.js') || f === 'style.css').sort() : [];
const missingProbe = EXPECTED_PROBE.filter(f => !probeFiles.includes(f));
if (missingProbe.length) warn(`probe sources not written yet: ${missingProbe.join(', ')}`);
if (fs.existsSync(probeDir)) {
  const ignored = fs.readdirSync(probeDir).filter(f => !probeFiles.includes(f));
  if (ignored.length) warn(`probe files not copied (only *.js and style.css are published): ${ignored.join(', ')}`);
}

const compress = compressJson();
for (const v of ['v1', 'v2']) {
  put(v, 'index.html', fragment(v));
  put(v, 'lock.json', `${JSON.stringify(lock, null, 1)}\n`);
  put(v, 'version.json', `${JSON.stringify({ version: v })}\n`);
  put(v, `data/${v}-only.json`, `${JSON.stringify({ version: v, file: `${v}-only`, note: `Published only in ${v}.` })}\n`);
  put(v, 'data/compress.json', compress);
  for (const f of probeFiles) put(v, f, fs.readFileSync(path.join(probeDir, f)));
  const [from, to] = v === 'v1' ? [1, 200] : [201, 300];
  for (let n = from; n <= to; n++) put(v, `bulk/b-${String(n).padStart(3, '0')}.json`, `${JSON.stringify({ n })}\n`);
}
// The third publish (platform.publish-omit-page) adds one data file and passes no page.
put('v3', 'data/v3-only.json', `${JSON.stringify({ version: 'v3', file: 'v3-only', note: 'Added by the third publish, which omits the page.' })}\n`);

const dbDir = path.join(ROOT, '..', 's1-dbsize'); // spikes/s1-dbsize, beside this spike
if (!fs.existsSync(path.join(dbDir, 'page.html'))) {
  warn('s1-dbsize/page.html not written yet: dist/dbsize/ is empty');
  fs.mkdirSync(path.join(DIST, 'dbsize'), { recursive: true });
  written.set('dbsize', []);
} else {
  put('dbsize', 'index.html', fs.readFileSync(path.join(dbDir, 'page.html')));
  for (const f of fs.readdirSync(dbDir).sort()) {
    if (f === 'page.html') continue;
    if (!ALLOWED_EXT.has(path.extname(f)) || !fs.statSync(path.join(dbDir, f)).isFile()) {
      warn(`s1-dbsize/${f} not copied: not a publishable file type`);
      continue;
    }
    put('dbsize', f, fs.readFileSync(path.join(dbDir, f)));
  }
  const js = fs.readdirSync(dbDir).filter(f => f.endsWith('.js'));
  if (!js.length) warn('s1-dbsize has no *.js files yet');
}

// ---- checks on what was written

const problems = [];
const manifest = { note: 'SHA-256 of every file tools/build.mjs wrote. Deterministic: rebuilding gives the same values.', folders: {} };
for (const [folder, files] of written) {
  manifest.folders[folder] = [];
  for (const { path: p, abs } of files.sort((a, b) => a.path.localeCompare(b.path))) {
    const buf = fs.readFileSync(abs);
    if (!ALLOWED_EXT.has(path.extname(p))) problems.push(`${folder}/${p}: extension not allowed`);
    if (buf.length > MAX_FILE_BYTES) problems.push(`${folder}/${p}: ${buf.length} bytes is over 1 MB`);
    if (/\.(m?js)$/.test(p)) {
      // Every published script parses as an ES module (classic worker scripts parse the same way).
      const r = spawnSync(process.execPath, ['--input-type=module', '--check'], { input: buf, encoding: 'utf8' });
      if (r.status !== 0) problems.push(`${folder}/${p}: does not parse: ${(r.stderr || '').trim().split('\n').slice(0, 6).join(' | ')}`);
    }
    if (p.endsWith('.json')) {
      try { JSON.parse(buf.toString('utf8')); } catch (e) { problems.push(`${folder}/${p}: invalid JSON: ${e.message}`); }
    }
    manifest.folders[folder].push({ path: p, bytes: buf.length, sha256: sha256(buf) });
  }
}

// Every page published as a fragment: no document tags, no module script, the title first.
const pages = [['v1', 'index.html', 'Spike S1 Probe'], ['v2', 'index.html', 'Spike S1 Probe'], ['dbsize', 'index.html', null]];
for (const [folder, file, title] of pages) {
  const p = path.join(DIST, folder, file);
  if (!fs.existsSync(p)) continue;
  const html = fs.readFileSync(p, 'utf8');
  if (/<\/?(html|head|body)[\s>]/i.test(html)) problems.push(`${folder}/${file}: contains html, head or body tags`);
  if (/<script[^>]*type=["']?module/i.test(html)) problems.push(`${folder}/${file}: contains a module script`);
  if (title ? !html.startsWith(`<title>${title}</title>`) : !/^<title>[^<]+<\/title>/.test(html)) problems.push(`${folder}/${file}: does not start with its title`);
}
for (const v of ['v1', 'v2']) {
  const count = manifest.folders[v].length;
  if (count > MAX_PATHS) problems.push(`${v}: ${count} paths, more than the ${MAX_PATHS} one publish may send`);
}
const mapMatch = fs.readFileSync(path.join(DIST, 'v1', 'index.html'), 'utf8').match(new RegExp(`<script type="importmap" id="${MAP_ID}">([\\s\\S]*?)</script>`));
if (!mapMatch) fail(`v1/index.html has no import map with id ${MAP_ID}`);
const map = JSON.parse(mapMatch[1]);
for (const [spec, url] of Object.entries(map.imports)) {
  if (!map.integrity[url]) problems.push(`import map: ${spec} has no integrity entry`);
  else if (url !== badIntegrity.url && map.integrity[url] !== verified.get(url)) problems.push(`import map: ${spec} integrity differs from npm`);
}
if (map.integrity[control.url]) problems.push('import map: the control URL must not have an integrity entry');
if (map.integrity[badIntegrity.second.url] !== badIntegrity.second.integrity) problems.push('import map: the second wrong-hash URL is not listed with its wrong hash');
const walk = closureProblems();
if (Array.isArray(walk)) problems.push(...walk);
else problems.push(...walk.problems);
const c1 = manifest.folders.v1.find(f => f.path === 'data/compress.json').sha256;
const c2 = manifest.folders.v2.find(f => f.path === 'data/compress.json').sha256;
if (c1 !== c2) problems.push('data/compress.json differs between v1 and v2');

// ---- the publish plan (CONTRACT.md, the runbook)

const v1 = new Map(manifest.folders.v1.map(f => [f.path, f.sha256]));
const v2 = new Map(manifest.folders.v2.map(f => [f.path, f.sha256]));
const added = [...v2.keys()].filter(p => !v1.has(p));
const changed = [...v2.keys()].filter(p => v1.has(p) && v1.get(p) !== v2.get(p));
const removed = [...v1.keys()].filter(p => !v2.has(p));
manifest.republish = {
  note: 'Paths for the v2 publish to the v1 Artifact: added and changed files are passed, removed paths are passed as null.',
  added,
  changed,
  removed,
  unchanged: [...v2.keys()].filter(p => v1.get(p) === v2.get(p)).length,
};
// The page counts as one of the files a publish sends [our choice: the conservative reading].
const changedFiles = changed.filter(p => p !== 'index.html');
const v2Entries = 1 + changedFiles.length + added.length + removed.length;
// The removals platform.version-scoping and platform.version-files read go first.
const FIRST = ['data/v1-only.json', 'bulk/b-001.json'];
const ordered = [...FIRST.filter(p => removed.includes(p)), ...removed.filter(p => !FIRST.includes(p))];
const room = MAX_PATHS - 1 - changedFiles.length - added.length;
if (room < FIRST.length) problems.push(`publish plan: the first fallback batch has room for ${room} removals, fewer than ${FIRST.length}`);
manifest.publishPlan = {
  note: 'Follow CONTRACT.md, the runbook. Sizes count the page as one file.',
  v1: { filePath: 'dist/v1/index.html', files: manifest.folders.v1.length - 1, entries: manifest.folders.v1.length, capabilities: PROBE_CAPABILITIES },
  v2: {
    filePath: 'dist/v2/index.html', files: { changed: changedFiles, added: added.length, nullRemovals: removed.length }, entries: v2Entries,
    overLimitIfNullsCount: v2Entries > MAX_PATHS,
  },
  v2FallbackBatches: v2Entries <= MAX_PATHS ? [] : [
    { filePath: 'dist/v2/index.html', files: [...changedFiles, ...added], nullRemovals: ordered.slice(0, room), entries: 1 + changedFiles.length + added.length + Math.min(room, ordered.length) },
    { filePath: 'dist/v2/index.html', files: [], nullRemovals: ordered.slice(room), entries: 1 + Math.max(0, ordered.length - room) },
  ],
  v3: { filePath: null, files: ['data/v3-only.json'], source: 'dist/v3/data/v3-only.json', entries: 1 },
  dbsize: { filePath: 'dist/dbsize/index.html', files: (manifest.folders.dbsize ?? []).filter(f => f.path !== 'index.html').map(f => f.path), capabilities: DBSIZE_CAPABILITIES },
};
fs.writeFileSync(path.join(DIST, 'manifest.json'), `${JSON.stringify(manifest, null, 1)}\n`);

// ---- report

for (const [folder, files] of Object.entries(manifest.folders)) {
  const bytes = files.reduce((a, f) => a + f.bytes, 0);
  console.log(`dist/${folder}: ${files.length} files, ${bytes} bytes`);
}
const r = manifest.republish;
console.log(`v1 to v2: ${r.added.length} added, ${r.changed.length} changed, ${r.removed.length} removed, ${r.unchanged} unchanged; ${v2Entries} entries with the page${v2Entries > MAX_PATHS ? `, so ${manifest.publishPlan.v2FallbackBatches.length} fallback batches` : ''}`);
console.log(`import map: ${Object.keys(map.imports).length} imports, ${Object.keys(map.integrity).length} integrity entries; the closure walk reached ${Array.isArray(walk) ? '?' : walk.reached} URLs`);
if (problems.length) {
  for (const p of problems) console.error(`build: problem: ${p}`);
  process.exit(1);
}
if (warnings.length) {
  console.log(`build finished with ${warnings.length} warning(s).`);
  if (STRICT) process.exit(1);
} else console.log('build finished: every check passed.');
