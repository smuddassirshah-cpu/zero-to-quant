// usage: node runpy.mjs script.py [datadir] [extra,files] ; Pyodide from local pkgs
import fs from 'fs'; import path from 'path'; import {createRequire} from 'module';
const root='/tmp/claude-0/-home-user-zero-to-quant/024bfe09-7a97-56c3-837c-b47a15727adf/scratchpad/pkgs/pyodide-0.27.7/package/';
const require=createRequire(root);
const {loadPyodide}=require(root+'pyodide.js');
const py=await loadPyodide({indexURL:root, stdout:s=>console.log(s), stderr:s=>console.log(s)});
const script=fs.readFileSync(process.argv[2],'utf8');
const dd=process.argv[3];
py.FS.mkdirTree('/work/data');
if(dd){for(const f of fs.readdirSync(dd)){const p=path.join(dd,f); if(fs.statSync(p).isFile()){py.FS.writeFile('/work/data/'+f, fs.readFileSync(p)); py.FS.writeFile('/work/'+f, fs.readFileSync(p));}}}
for(const f of (process.argv[4]||'').split(',').filter(Boolean)){py.FS.writeFile('/work/'+path.basename(f), fs.readFileSync(f));}
py.FS.chdir('/work');
await py.loadPackage(['numpy','pandas','scipy','scikit-learn','statsmodels']);
py.runPython('import sys; sys.path.insert(0,"/work")');
await py.runPythonAsync(script);
