// Pyodide in a worker, with archives reassembled in memory from published text and .wasm parts.
const BASE = new URL('./py/', self.location.href).href;
const enc = new TextEncoder();
const crcTable = (() => { const t = new Uint32Array(256); for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } return t; })();
const crc32 = (b) => { let c = 0xFFFFFFFF; for (let i = 0; i < b.length; i++) c = crcTable[(c ^ b[i]) & 0xFF] ^ (c >>> 8); return (c ^ 0xFFFFFFFF) >>> 0; };
// Store-only zip writer: enough for Pyodide's unpacker, no compression needed in memory.
function zip(entries) {
  const chunks = [], central = []; let off = 0;
  for (const [name, data] of entries) {
    const n = enc.encode(name), crc = crc32(data), h = new DataView(new ArrayBuffer(30));
    h.setUint32(0, 0x04034b50, true); h.setUint16(4, 20, true); h.setUint32(14, crc, true); h.setUint32(18, data.length, true); h.setUint32(22, data.length, true); h.setUint16(26, n.length, true);
    chunks.push(new Uint8Array(h.buffer), n, data);
    const c = new DataView(new ArrayBuffer(46));
    c.setUint32(0, 0x02014b50, true); c.setUint16(4, 20, true); c.setUint16(6, 20, true); c.setUint32(16, crc, true); c.setUint32(20, data.length, true); c.setUint32(24, data.length, true); c.setUint16(28, n.length, true); c.setUint32(42, off, true);
    central.push(new Uint8Array(c.buffer), n); off += 30 + n.length + data.length;
  }
  const cdSize = central.reduce((s, a) => s + a.length, 0), e = new DataView(new ArrayBuffer(22));
  e.setUint32(0, 0x06054b50, true); e.setUint16(8, entries.length, true); e.setUint16(10, entries.length, true); e.setUint32(12, cdSize, true); e.setUint32(16, off, true);
  const all = [...chunks, ...central, new Uint8Array(e.buffer)], out = new Uint8Array(all.reduce((s, a) => s + a.length, 0));
  let p = 0; for (const a of all) { out.set(a, p); p += a.length; } return out;
}
const realFetch = self.fetch.bind(self);
let manifest = null;
async function assemble(file) {
  const m = manifest[file]; if (!m) return null;
  const texts = await (await realFetch(BASE + m.json)).json();
  const b64 = (s) => Uint8Array.from(atob(s), (ch) => ch.charCodeAt(0));
  const entries = await Promise.all(m.parts.map(async (p) => [p.path, p.text ? enc.encode(texts[p.path]) : p.b64 ? b64(texts[p.path]) : new Uint8Array(await (await realFetch(BASE + p.wasm)).arrayBuffer())]));
  return zip(entries);
}
self.fetch = async (input, init) => {
  const url = input instanceof Request ? input.url : String(input), file = url.split('/').pop().split('?')[0];
  if (manifest && manifest[file]) return new Response(await assemble(file), { status: 200, headers: { 'Content-Type': 'application/octet-stream' } });
  return realFetch(input, init);
};
self.onmessage = async (e) => {
  const t0 = performance.now(), log = (m) => self.postMessage({ log: m, ms: Math.round(performance.now() - t0) });
  try {
    manifest = await (await realFetch(BASE + 'manifest.json')).json(); log('manifest');
    const { loadPyodide } = await import(BASE + 'pyodide.mjs'); log('module');
    const py = await loadPyodide({ indexURL: BASE }); log('python ' + py.runPython('import sys; sys.version.split()[0]'));
    await py.loadPackage(e.data.packages || [], { messageCallback: () => {}, checkIntegrity: false }); log('packages ' + (e.data.packages || []).join(','));
    const out = py.runPython(e.data.code); log('result ' + out);
    self.postMessage({ done: true, ms: Math.round(performance.now() - t0) });
  } catch (err) { self.postMessage({ error: String(err && err.message || err).slice(0, 400), ms: Math.round(performance.now() - t0) }); }
};
