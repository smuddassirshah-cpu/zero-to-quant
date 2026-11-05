import fs from 'fs';
import { WASI } from 'node:wasi';
const [wf, idx, outf, errf] = process.argv.slice(2);
const mod = await WebAssembly.compile(fs.readFileSync(wf));
const fd = fs.openSync(outf, 'w+'), fe = fs.openSync(errf, 'w+');
const wasi = new WASI({ version: 'preview1', args: ['a', idx], stdout: fd, stderr: fe, returnOnExit: true });
let code = 0;
try { const inst = await WebAssembly.instantiate(mod, { wasi_snapshot_preview1: wasi.wasiImport }); code = wasi.start(inst); } catch (e) { fs.writeSync(fe, 'TRAP ' + (e.message || e)); code = 99; }
process.exitCode = code;
