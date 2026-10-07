// One configuration, three modes (ARCHITECTURE.md 6.1): `web` and `artifact` are production
// builds, `dev` is the development server. Each target has its own page head in src/html/.
import { fileURLToPath } from 'node:url';
import { defineConfig, type Plugin } from 'vite';

type Mode = 'web' | 'artifact' | 'dev';

const repo = fileURLToPath(new URL('.', import.meta.url));

function isMode(mode: string): mode is Mode {
  return mode === 'web' || mode === 'artifact' || mode === 'dev';
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

// The dev server has no root index.html; `/` redirects to the development page so that the
// page's relative script and stylesheet paths resolve as they do in the builds.
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
      res.setHeader('Location', `/src/html/dev.html${req.url.slice(1)}`);
      res.end();
    });
  },
};

export default defineConfig(({ mode }) => {
  if (!isMode(mode)) throw new Error(`Unknown mode "${mode}": use web, artifact or dev`);
  const target = mode === 'artifact' ? 'artifact' : 'web';
  const page = `src/html/${target}.html`;
  return {
    root: repo,
    publicDir: false,
    base: mode === 'artifact' ? './' : (process.env.VITE_BASE ?? '/'),
    resolve: { alias: { '@': `${repo}src` } },
    define: {
      __TARGET__: JSON.stringify(target),
      __DEV_ROUTES__: JSON.stringify(mode === 'dev'),
    },
    plugins: [pageAsIndex(page), devIndex],
    build: {
      outDir: `${repo}dist/${target}`,
      emptyOutDir: true,
      target: 'es2022',
      cssCodeSplit: false,
      modulePreload: { polyfill: false },
      // Fonts and WebAssembly always load as their own files (ARCHITECTURE.md 6.1).
      assetsInlineLimit: (file: string) => (/\.(woff2?|ttf|otf|wasm)$/.test(file) ? false : undefined),
      sourcemap: mode === 'web' ? 'hidden' : false,
      manifest: mode === 'artifact',
      rolldownOptions: {
        input: { app: `${repo}${page}` },
        output: {
          entryFileNames: 'assets/[name].[hash].js',
          chunkFileNames: 'assets/[name].[hash].js',
          // cssCodeSplit is off, so the one stylesheet is the app's (ARCHITECTURE.md 6.2.1).
          assetFileNames: (info) =>
            info.names.includes('style.css') ? 'assets/app.[hash][extname]' : 'assets/[name].[hash][extname]',
        },
      },
    },
  };
});
