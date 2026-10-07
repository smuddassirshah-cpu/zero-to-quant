// One configuration, three modes (ARCHITECTURE.md 6.1): `web` and `artifact` are production builds,
// `dev` is the development server. Decision notes:
// - Builds use `src/html` as the root, so each page sits at the depth of its output and Vite's relative
//   asset paths (`./assets/...` with base `./`) are right in the published folder.
// - The dev server uses `src` as the root and may read only `src/` and `node_modules/`: with the
//   repository as root, files such as `.dev.vars` and `proxy/.state/` were served [measured in review].
// - `VITE_BASE` comes from `.env` files through `loadEnv`, as ARCHITECTURE.md 11.4 says.
import { mkdirSync, readdirSync, renameSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { defineConfig, loadEnv, type Plugin } from 'vite';

type Mode = 'web' | 'artifact' | 'dev';

const repo = fileURLToPath(new URL('.', import.meta.url));
const src = join(repo, 'src');

function isMode(mode: string): mode is Mode {
  return mode === 'web' || mode === 'artifact' || mode === 'dev';
}

function webBase(value: string | undefined): string {
  const base = value === undefined || value === '' ? '/' : value;
  if (!base.startsWith('/') || !base.endsWith('/')) throw new Error(`VITE_BASE must start and end with "/"`);
  return base;
}

// Vite names an HTML output after its path under `root`; both targets publish `index.html`.
function pageAsIndex(page: string): Plugin {
  return {
    name: 'zq-page-as-index',
    apply: 'build',
    enforce: 'post',
    generateBundle(_options, bundle) {
      const out = bundle[page];
      if (!out) this.error(`Expected the page ${page} in the bundle`);
      out.fileName = 'index.html';
    },
  };
}

// Hidden source maps are CI artefacts, never deployed: move them out of the published folder.
function mapsOutOf(outDir: string, mapsDir: string): Plugin {
  return {
    name: 'zq-maps-out',
    apply: 'build',
    closeBundle() {
      for (const entry of readdirSync(outDir, { recursive: true, withFileTypes: true })) {
        if (!entry.isFile() || !entry.name.endsWith('.map')) continue;
        const from = join(entry.parentPath, entry.name);
        const to = join(mapsDir, from.slice(outDir.length));
        mkdirSync(dirname(to), { recursive: true });
        renameSync(from, to);
      }
    },
  };
}

// The dev server has no index page; `/` redirects to the development page.
const devIndex: Plugin = {
  name: 'zq-dev-index',
  apply: 'serve',
  configureServer(server) {
    server.middlewares.use((req, res, next) => {
      if (req.url !== '/' && !req.url?.startsWith('/?')) {
        next();
        return;
      }
      res.statusCode = 302;
      res.setHeader('Location', `/html/dev.html${req.url.slice(1)}`);
      res.end();
    });
  },
};

export default defineConfig(({ mode }) => {
  if (!isMode(mode)) throw new Error(`Unknown mode "${mode}": use web, artifact or dev`);
  const env = loadEnv(mode, repo, 'VITE_');
  const target = mode === 'artifact' ? 'artifact' : 'web';
  const outDir = join(repo, 'dist', target);
  const naming = {
    entryFileNames: 'assets/[name].[hash].js',
    chunkFileNames: 'assets/[name].[hash].js',
    // cssCodeSplit is off, so the one stylesheet is the app's (ARCHITECTURE.md 6.2.1).
    assetFileNames: (info: { names: readonly string[] }) =>
      info.names.includes('style.css') ? 'assets/app.[hash][extname]' : 'assets/[name].[hash][extname]',
  };
  return {
    root: mode === 'dev' ? src : join(src, 'html'),
    envDir: repo,
    publicDir: false,
    base: mode === 'artifact' ? './' : mode === 'dev' ? '/' : webBase(env.VITE_BASE),
    resolve: { alias: { '@': src } },
    define: {
      __TARGET__: JSON.stringify(target),
      // Preview Artifacts compile the development routes in too (ARCHITECTURE.md 6.5, stage 25).
      __DEV_ROUTES__: JSON.stringify(mode === 'dev' || process.env.ZQ_DEV_ROUTES === '1'),
    },
    server: {
      fs: {
        strict: true,
        allow: [src, join(repo, 'node_modules')],
        deny: ['.env', '.env.*', '.dev.vars*', '*.{crt,pem,key}', '**/.git/**', '**/proxy/.state/**'],
      },
    },
    plugins: [pageAsIndex(`${target}.html`), mapsOutOf(outDir, join(repo, 'dist', 'maps', target)), devIndex],
    worker: { format: 'es', rolldownOptions: { output: naming } },
    build: {
      outDir,
      emptyOutDir: true,
      target: 'es2022',
      cssCodeSplit: false,
      modulePreload: { polyfill: false },
      // Fonts and WebAssembly always load as their own files (ARCHITECTURE.md 6.1).
      assetsInlineLimit: (file: string) => (/\.(woff2?|ttf|otf|wasm)$/.test(file) ? false : undefined),
      sourcemap: mode === 'web' ? 'hidden' : false,
      manifest: mode === 'artifact',
      rolldownOptions: { input: { app: join(src, 'html', `${target}.html`) }, output: naming },
    },
  };
});
