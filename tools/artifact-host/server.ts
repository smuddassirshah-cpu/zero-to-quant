// Minimal local stand-in for the Artifact host (docs/ARCHITECTURE.md 8.2):
// `node tools/artifact-host/server.ts <dir> [--port <n>]`, bound to 127.0.0.1. Decision notes:
// - Only the host's served types, and only regular files inside `<dir>`: the request path is decoded
//   once, refused if it holds a NUL or a backslash, resolved, and must stay inside the folder. Links are
//   not followed, so nothing outside the build can be reached through one.
// - `/` and `/index.html` return the published fragment inside a document skeleton, as the host wraps a
//   published page.
// - Stage 4 completes the emulator: the CSP header, the sandboxed second origin, the fake window.claude
//   and the locked CDN modules served from local copies.
import { existsSync } from 'node:fs';
import { lstat, readFile } from 'node:fs/promises';
import { createServer, type IncomingMessage, type Server, type ServerResponse } from 'node:http';
import type { AddressInfo } from 'node:net';
import { extname, join, resolve, sep } from 'node:path';
import { parseArgs } from 'node:util';

export const HOST = '127.0.0.1';
export const DEFAULT_PORT = 4174;
const USAGE = 'Usage: node tools/artifact-host/server.ts <dir> [--port <n>]';

export const SERVED_TYPES: ReadonlyMap<string, string> = new Map([
  ['.html', 'text/html; charset=utf-8'],
  ['.js', 'text/javascript; charset=utf-8'],
  ['.mjs', 'text/javascript; charset=utf-8'],
  ['.css', 'text/css; charset=utf-8'],
  ['.json', 'application/json; charset=utf-8'],
  ['.svg', 'image/svg+xml'],
]);

export function wrapPage(fragment: string): string {
  return (
    '<!doctype html><html lang="en-GB"><head>' +
    '<meta name="viewport" content="width=device-width, initial-scale=1">' +
    `</head><body>${fragment}</body></html>`
  );
}

/** The file a request target names inside `root`, or undefined when it names none or leaves `root`. */
export function resolveRequestPath(root: string, target: string): string | undefined {
  const pathname = target.split(/[?#]/, 1)[0] ?? '';
  if (!pathname.startsWith('/')) return undefined;
  let decoded: string;
  try {
    decoded = decodeURIComponent(pathname);
  } catch (error) {
    if (error instanceof URIError) return undefined;
    throw error;
  }
  if (decoded.includes('\0') || decoded.includes('\\')) return undefined;
  const file = resolve(root, decoded.slice(1) || 'index.html');
  return file.startsWith(root + sep) ? file : undefined;
}

async function isRegularFile(path: string): Promise<boolean> {
  try {
    return (await lstat(path)).isFile();
  } catch (error) {
    const code = (error as NodeJS.ErrnoException).code;
    if (code === 'ENOENT' || code === 'ENOTDIR') return false;
    throw error;
  }
}

function send(res: ServerResponse, status: number, text: string): void {
  res.writeHead(status, { 'Content-Type': 'text/plain; charset=utf-8', 'Cache-Control': 'no-store' });
  res.end(text);
}

async function respond(root: string, req: IncomingMessage, res: ServerResponse): Promise<void> {
  if (req.method !== 'GET' && req.method !== 'HEAD') {
    res.setHeader('Allow', 'GET, HEAD');
    send(res, 405, 'Method not allowed');
    return;
  }
  const file = resolveRequestPath(root, req.url ?? '/');
  const type = file === undefined ? undefined : SERVED_TYPES.get(extname(file));
  if (file === undefined || type === undefined || !(await isRegularFile(file))) {
    send(res, 404, 'Not found');
    return;
  }
  const body =
    file === join(root, 'index.html') ? wrapPage(await readFile(file, 'utf8')) : await readFile(file);
  res.writeHead(200, {
    'Content-Type': type,
    'Content-Length': Buffer.byteLength(body),
    'Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff',
  });
  res.end(req.method === 'HEAD' ? undefined : body);
}

export function createHost(dir: string): Server {
  const root = resolve(dir);
  return createServer((req, res) => {
    respond(root, req, res).catch((error: unknown) => {
      console.error('artifact-host: request failed', error);
      if (res.headersSent) res.destroy();
      else send(res, 500, 'Internal error');
    });
  });
}

export function parseHostArgs(argv: readonly string[]): { dir: string; port: number } {
  const { values, positionals } = parseArgs({
    args: [...argv],
    options: { port: { type: 'string' } },
    allowPositionals: true,
  });
  const [dir] = positionals;
  if (positionals.length !== 1 || dir === undefined) throw new Error(USAGE);
  const port = values.port ?? String(DEFAULT_PORT);
  if (!/^\d{1,5}$/.test(port) || Number(port) > 65_535) throw new Error(`Invalid --port: ${port}`);
  return { dir, port: Number(port) };
}

export function main(argv: readonly string[]): Server {
  const { dir, port } = parseHostArgs(argv);
  if (!existsSync(join(dir, 'index.html'))) {
    throw new Error(`No index.html in ${dir}: build the Artifact first`);
  }
  const server = createHost(dir);
  server.listen(port, HOST, () => {
    console.log(`Artifact host: http://${HOST}:${(server.address() as AddressInfo).port}/ serving ${dir}`);
  });
  return server;
}

if (import.meta.main) main(process.argv.slice(2));
