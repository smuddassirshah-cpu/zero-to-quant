// Spike S1 host emulator: serves one dist folder on loopback the way the Artifact host serves a page.
//
// Usage: node tools/serve.mjs <distDir> [--port N] [--no-csp]
//   GET / and /index.html  the fragment wrapped in the host's document skeleton
//   GET /<path>            a file under the root, allowed types only, Cache-Control: no-store
//   POST /__switch?dir=D   serve another dist folder from now on (emulates a republish); D must sit
//                          under the same parent as the starting root
//
// Decision notes:
// - Loopback only (127.0.0.1); there is no option to bind elsewhere.
// - Containment is checked on real paths, so neither `..` nor a symbolic link can leave the root.
// - The CSP header is our reading of the host rules in CONTRACT.md [inferred], not a copy of the
//   host's measured header: scripts from our files and the CDN hosts, styles from our files and
//   Google Fonts, fetch to our own origin only, workers from our files or blob:. --no-csp drops it.

import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
};

export const HOST_CSP = [
  "default-src 'none'",
  "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net/npm/ https://cdnjs.cloudflare.com https://unpkg.com https://cdn.tailwindcss.com https://code.jquery.com",
  "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
  'font-src https://fonts.gstatic.com',
  "connect-src 'self'",
  "worker-src 'self' blob:",
  "img-src 'self' data: blob:",
  "frame-src 'none'",
  "object-src 'none'",
  "base-uri 'self'",
  "form-action 'none'",
].join('; ');

// The host's skeleton, byte for byte [measured: the published v1 page read back, 7 October 2026].
const HOST_HEAD = '<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"><style>'
  + ':root{color-scheme:light;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
  + 'html{scroll-padding-top:env(safe-area-inset-top,0px)}body{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif;background:#faf9f5;color:#141413}'
  + 'img{max-width:100%}[hidden]:not([hidden=until-found i]){display:none!important}</style></head><body>\n';

export function wrapFragment(fragment) {
  return `${HOST_HEAD}${fragment}\n</body></html>`;
}

const realDir = dir => {
  const real = fs.realpathSync(path.resolve(dir));
  if (!fs.statSync(real).isDirectory()) throw new Error(`${dir} is not a directory`);
  return real;
};
const inside = (base, p) => p === base || p.startsWith(base + path.sep);

/**
 * Starts the emulator and resolves once it listens.
 * @param {{ root: string, port?: number, csp?: boolean, allowBase?: string, log?: (line: string) => void }} options
 * @returns {Promise<{ url: string, port: number, server: http.Server, getRoot(): string, setRoot(dir: string): string, close(): Promise<void> }>}
 */
export async function createServer({ root, port = 0, csp = true, allowBase, log = () => {} }) {
  let current = realDir(root);
  const base = realDir(allowBase ?? path.dirname(current));

  const setRoot = dir => {
    if (!path.isAbsolute(dir)) throw new Error('dir must be an absolute path');
    const next = realDir(dir);
    if (!inside(base, next)) throw new Error(`dir must be under ${base}`);
    current = next;
    log(`root is now ${current}`);
    return current;
  };

  const send = (res, status, type, body, head = false) => {
    const headers = { 'Content-Type': type, 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' };
    if (csp) headers['Content-Security-Policy'] = HOST_CSP;
    res.writeHead(status, headers);
    res.end(head ? undefined : body);
  };
  const notFound = (res, head) => send(res, 404, 'text/plain; charset=utf-8', 'Not found\n', head);

  const server = http.createServer((req, res) => {
    let url;
    try {
      url = new URL(req.url, 'http://127.0.0.1');
    } catch (e) {
      log(`bad request URL: ${e.message}`);
      return send(res, 400, 'text/plain; charset=utf-8', 'Bad request\n');
    }

    if (req.method === 'POST' && url.pathname === '/__switch') {
      req.resume();
      try {
        const now = setRoot(url.searchParams.get('dir') ?? '');
        return send(res, 200, 'application/json; charset=utf-8', `${JSON.stringify({ root: now })}\n`);
      } catch (e) {
        log(`switch refused: ${e.message}`);
        return send(res, 400, 'application/json; charset=utf-8', `${JSON.stringify({ error: e.message })}\n`);
      }
    }
    if (req.method !== 'GET' && req.method !== 'HEAD') return send(res, 405, 'text/plain; charset=utf-8', 'Method not allowed\n');
    const head = req.method === 'HEAD';

    let pathname;
    try {
      pathname = decodeURIComponent(url.pathname);
    } catch (e) {
      log(`bad path encoding: ${e.message}`);
      return notFound(res, head);
    }
    if (pathname.includes('\0')) return notFound(res, head);

    if (pathname === '/' || pathname === '/index.html') {
      const file = path.join(current, 'index.html');
      let fragment;
      try {
        fragment = fs.readFileSync(file, 'utf8');
      } catch (e) {
        log(`no index.html in ${current}: ${e.code ?? e.message}`);
        return notFound(res, head);
      }
      return send(res, 200, TYPES['.html'], wrapFragment(fragment), head);
    }

    const type = TYPES[path.extname(pathname).toLowerCase()];
    if (!type) return notFound(res, head);
    let real;
    try {
      real = fs.realpathSync(path.join(current, pathname));
    } catch (e) {
      if (e.code !== 'ENOENT' && e.code !== 'ENOTDIR') log(`realpath ${pathname}: ${e.code ?? e.message}`);
      return notFound(res, head);
    }
    if (!inside(current, real) || !fs.statSync(real).isFile()) return notFound(res, head);
    return send(res, 200, type, fs.readFileSync(real), head);
  });

  await new Promise((resolve, reject) => {
    server.once('error', reject);
    server.listen(port, '127.0.0.1', () => { server.off('error', reject); resolve(); });
  });
  const actual = server.address().port;
  return {
    url: `http://127.0.0.1:${actual}/`,
    port: actual,
    server,
    getRoot: () => current,
    setRoot,
    close: () => new Promise((resolve, reject) => {
      server.closeAllConnections?.();
      server.close(e => (e ? reject(e) : resolve()));
    }),
  };
}

const isMain = process.argv[1] && import.meta.url === pathToFileURL(fs.realpathSync(process.argv[1])).href;
if (isMain) {
  const args = process.argv.slice(2);
  const dir = args.find((a, i) => !a.startsWith('--') && args[i - 1] !== '--port');
  const portIndex = args.indexOf('--port');
  const port = portIndex >= 0 ? Number(args[portIndex + 1]) : 4311;
  if (!dir || !Number.isInteger(port) || port < 0 || port > 65535) {
    console.error('usage: node tools/serve.mjs <distDir> [--port N] [--no-csp]');
    process.exit(2);
  }
  const s = await createServer({ root: dir, port, csp: !args.includes('--no-csp'), log: line => console.log(`serve: ${line}`) });
  console.log(`serve: ${s.getRoot()} at ${s.url}`);
  const stop = () => s.close().then(() => process.exit(0), e => { console.error(`serve: close failed: ${e.message}`); process.exit(1); });
  process.on('SIGINT', stop);
  process.on('SIGTERM', stop);
}
