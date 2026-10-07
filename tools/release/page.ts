// Rewrites Vite's Artifact `index.html` as the page fragment the host wraps (docs/ARCHITECTURE.md 6.2.2):
// `node tools/release/page.ts dist/artifact`. Decision notes:
// - The entry and stylesheet come from Vite's manifest and must match a strict pattern before they
//   reach the HTML, so the fragment needs no escaping.
// - Two classic inline scripts, as ARCHITECTURE.md 6.2.2 lists them. The ES5 gate (3.3) shows its message
//   and sets `window.__zqOld`; the bootstrap returns on that flag, otherwise it runs a page-level dynamic
//   import() of the entry, the path the Artifact probe measured (no <script type="module">). Kept apart,
//   an engine that cannot parse import() still runs the gate.
// - `<div id="app">` comes before the gate, which writes into it; 6.2.2 lists it after the import map.
// - The manifest moves to `<dir>-manifest.json` and `.vite/` is removed: the release folder holds only
//   published files, and later release steps still find the manifest beside it.
import { existsSync, readFileSync, renameSync, rmSync, writeFileSync } from 'node:fs';
import { join, relative, resolve } from 'node:path';

export interface PageAssets {
  readonly entry: string;
  readonly stylesheet: string;
}

const ASSET = /^assets\/[A-Za-z0-9._-]+\.(js|css)$/;
const FONTS =
  'https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=Besley:ital,wght@0,400..900;1,400..900&family=Source+Code+Pro:wght@400;500;700&display=swap';
const USAGE = 'Usage: node tools/release/page.ts <dir>';

function checkAsset(path: string, kind: 'js' | 'css'): void {
  if (ASSET.exec(path)?.[1] !== kind) {
    throw new Error(`Refusing ${JSON.stringify(path)} as the page's ${kind} asset`);
  }
}

export function renderPage({ entry, stylesheet }: PageAssets): string {
  checkAsset(entry, 'js');
  checkAsset(stylesheet, 'css');
  return [
    '<meta charset="utf-8">',
    '<title>Zero to Quant</title>',
    '<link rel="preconnect" href="https://fonts.googleapis.com">',
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
    `<link rel="stylesheet" href="${FONTS}">`,
    `<link rel="stylesheet" href="./${stylesheet}">`,
    '<div id="app"></div>',
    '<script>',
    "if (!(typeof structuredClone === 'function' && typeof [].at === 'function' &&",
    "    typeof CSS !== 'undefined' && CSS.supports('transition-timing-function', 'linear(0, 1)'))) {",
    '  window.__zqOld = true;',
    "  document.getElementById('app').textContent = 'This browser is too old for Zero to Quant.';",
    '}',
    '</script>',
    // Stage 4 inserts the <script type="importmap"> from cdn.lock.json here, before the bootstrap.
    '<script>',
    '(function () {',
    '  if (window.__zqOld) return;',
    `  import('./${entry}').catch(function (error) {`,
    "    document.getElementById('app').textContent = 'Zero to Quant could not start. Reload to try again.';",
    '    console.error(error);',
    '  });',
    '})();',
    '</script>',
    '',
  ].join('\n');
}

const isRecord = (value: unknown): value is Record<string, unknown> =>
  typeof value === 'object' && value !== null && !Array.isArray(value);

/** The single entry chunk and the `style.css` asset of a Vite manifest. */
export function readManifest(manifest: unknown): PageAssets {
  if (!isRecord(manifest)) throw new Error('The Vite manifest is not an object');
  const entries = Object.values(manifest).filter(
    (chunk): chunk is Record<string, unknown> => isRecord(chunk) && chunk.isEntry === true,
  );
  if (entries.length !== 1) {
    throw new Error(`Expected one entry chunk in the Vite manifest, found ${entries.length}`);
  }
  const entry = entries[0]?.file;
  const style = manifest['style.css'];
  const stylesheet = isRecord(style) ? style.file : undefined;
  if (typeof entry !== 'string') throw new Error('The entry chunk in the Vite manifest names no file');
  if (typeof stylesheet !== 'string') throw new Error('The Vite manifest has no style.css asset');
  return { entry, stylesheet };
}

export function main(argv: readonly string[], print: (line: string) => void = console.log): number {
  const [arg] = argv;
  if (argv.length !== 1 || arg === undefined) {
    print(USAGE);
    return 2;
  }
  const dir = resolve(arg);
  const manifestPath = join(dir, '.vite', 'manifest.json');
  if (!existsSync(manifestPath)) {
    print(`page: no Vite manifest at ${manifestPath}; run vite build --mode artifact first`);
    return 1;
  }
  const assets = readManifest(JSON.parse(readFileSync(manifestPath, 'utf8')));
  const html = renderPage(assets);
  for (const path of [assets.entry, assets.stylesheet]) {
    if (!existsSync(join(dir, path))) {
      print(`page: the manifest names ${path}, which is not in ${dir}`);
      return 1;
    }
  }
  const moved = `${dir}-manifest.json`;
  writeFileSync(join(dir, 'index.html'), html);
  renameSync(manifestPath, moved);
  rmSync(join(dir, '.vite'), { recursive: true });
  print(`page: wrote index.html for ${assets.entry}; manifest moved to ${relative(process.cwd(), moved)}`);
  return 0;
}

if (import.meta.main) process.exitCode = main(process.argv.slice(2));
