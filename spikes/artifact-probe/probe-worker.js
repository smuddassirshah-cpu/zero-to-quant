// Probe worker: echoes, then compiles a minimal WebAssembly module inside the worker.
self.onmessage = async (e) => {
  const out = { echo: e.data, wasm: null };
  try {
    const bytes = new Uint8Array([0,97,115,109,1,0,0,0,1,7,1,96,2,127,127,1,127,3,2,1,0,7,7,1,3,97,100,100,0,0,10,9,1,7,0,32,0,32,1,106,11]);
    const { instance } = await WebAssembly.instantiate(bytes);
    out.wasm = instance.exports.add(2, 3) === 5 ? 'ok' : 'wrong result';
  } catch (err) { out.wasm = 'blocked: ' + (err && err.message || err); }
  self.postMessage(out);
};
