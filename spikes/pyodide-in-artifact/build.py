"""Split Pyodide's stdlib zip and package wheels into servable parts:
text files go into one JSON map per archive; WebAssembly side modules (.so) are served as .wasm.
The page reassembles each archive in memory, so no archive file is ever published."""
import base64, json, os, sys, zipfile, shutil, hashlib
SRC_CORE, SRC_WHEELS, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT + '/py/pkgs')
for f in ['pyodide.mjs', 'pyodide.asm.mjs', 'pyodide.asm.wasm', 'pyodide-lock.json']:
    shutil.copy(os.path.join(SRC_CORE, f), OUT + '/py/' + f)
manifest = {}
def split(zpath, name):
    z = zipfile.ZipFile(zpath); texts = {}; parts = []
    for i in z.infolist():
        if i.is_dir() or i.filename.endswith('.a') or '/tests/' in i.filename or i.filename.endswith(('.pyi', '.c', '.h', '.pxd')): continue  # build-time and test files are not needed at runtime
        b = z.read(i.filename)
        if b[:4] == b'\0asm':
            safe = hashlib.sha1(i.filename.encode()).hexdigest()[:12] + '.wasm'
            open(f'{OUT}/py/pkgs/{name}-{safe}', 'wb').write(b)
            parts.append({'path': i.filename, 'wasm': f'pkgs/{name}-{safe}'})
        else:
            try: texts[i.filename] = b.decode('utf-8'); parts.append({'path': i.filename, 'text': True})
            except UnicodeDecodeError:  # small data files (time-zone tables) embed as base64, like a data: URI
                texts[i.filename] = base64.b64encode(b).decode(); parts.append({'path': i.filename, 'b64': True})
    json.dump(texts, open(f'{OUT}/py/pkgs/{name}.json', 'w'), separators=(',', ':'))
    manifest[os.path.basename(zpath)] = {'json': f'pkgs/{name}.json', 'parts': parts}
split(os.path.join(SRC_CORE, 'python_stdlib.zip'), 'stdlib')
for w in sorted(os.listdir(SRC_WHEELS)):
    if w.endswith('.whl'): split(os.path.join(SRC_WHEELS, w), w.split('-')[0])
json.dump(manifest, open(OUT + '/py/manifest.json', 'w'), separators=(',', ':'))
files = [os.path.join(dp, f) for dp, _, fs in os.walk(OUT) for f in fs]
print(len(files), 'files,', round(sum(os.path.getsize(f) for f in files) / 1e6, 1), 'MB; largest',
      sorted(((os.path.getsize(f) // 1000, os.path.basename(f)) for f in files), reverse=True)[:5])
