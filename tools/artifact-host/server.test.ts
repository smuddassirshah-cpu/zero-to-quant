import { mkdirSync, mkdtempSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import { request, type Server } from 'node:http';
import type { AddressInfo } from 'node:net';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterAll, beforeAll, describe, expect, it, vi } from 'vitest';
import { createHost, DEFAULT_PORT, main, parseHostArgs, resolveRequestPath, wrapPage } from './server.ts';

interface Reply {
  readonly status: number;
  readonly headers: Record<string, string | string[] | undefined>;
  readonly body: string;
}

const outer = mkdtempSync(join(tmpdir(), 'zq-host-'));
const root = join(outer, 'artifact');
const FRAGMENT = '<meta charset="utf-8">\n<title>Zero to Quant</title>\n<div id="app"></div>\n';
let server: Server;
let port: number;

// A raw request target, so neither fetch nor URL normalises the path before the server sees it.
function get(path: string, method = 'GET'): Promise<Reply> {
  return new Promise((done, fail) => {
    const req = request({ host: '127.0.0.1', port, path, method }, (res) => {
      let body = '';
      res.setEncoding('utf8');
      res.on('data', (chunk: string) => (body += chunk));
      res.on('end', () => {
        done({ status: res.statusCode ?? 0, headers: res.headers, body });
      });
    });
    req.on('error', fail);
    req.end();
  });
}

function listening(host: Server): Promise<number> {
  return new Promise((done) => {
    host.once('listening', () => {
      done((host.address() as AddressInfo).port);
    });
  });
}

beforeAll(async () => {
  mkdirSync(join(root, 'assets'), { recursive: true });
  writeFileSync(join(root, 'index.html'), FRAGMENT);
  for (const name of ['app.js', 'gen.mjs', 'app.css', 'data.json', 'icon.svg', 'core.wasm', 'notes.txt']) {
    writeFileSync(join(root, 'assets', name), `/* ${name} */`);
  }
  writeFileSync(join(outer, 'secret.js'), 'secret');
  symlinkSync(join(outer, 'secret.js'), join(root, 'assets', 'link.js'));
  server = createHost(root).listen(0, '127.0.0.1');
  port = await listening(server);
});

afterAll(() => {
  server.close();
  rmSync(outer, { recursive: true, force: true });
});

describe('the host', () => {
  it('wraps the published fragment in a document skeleton at / and /index.html', async () => {
    for (const path of ['/', '/index.html', '/?route=today']) {
      const reply = await get(path);
      expect(reply.status).toBe(200);
      expect(reply.headers['content-type']).toBe('text/html; charset=utf-8');
      expect(reply.headers['cache-control']).toBe('no-store');
      expect(reply.body).toBe(wrapPage(FRAGMENT));
    }
    expect(wrapPage('<p>x</p>')).toBe(
      '<!doctype html><html lang="en-GB"><head><meta name="viewport" content="width=device-width, initial-scale=1">' +
        '</head><body><p>x</p></body></html>',
    );
  });

  it.each([
    ['/assets/app.js', 'text/javascript; charset=utf-8'],
    ['/assets/gen.mjs', 'text/javascript; charset=utf-8'],
    ['/assets/app.css', 'text/css; charset=utf-8'],
    ['/assets/data.json', 'application/json; charset=utf-8'],
    ['/assets/icon.svg', 'image/svg+xml'],
    ['/assets/../assets/app.js', 'text/javascript; charset=utf-8'],
  ])('serves %s as %s', async (path, type) => {
    const reply = await get(path);
    expect(reply).toMatchObject({
      status: 200,
      headers: { 'content-type': type, 'cache-control': 'no-store' },
    });
    expect(reply.body).toMatch(/^\/\* /);
  });

  it.each([
    ['an unserved type', '/assets/notes.txt'],
    ['WebAssembly', '/assets/core.wasm'],
    ['a missing file', '/assets/missing.js'],
    ['a folder', '/assets'],
    ['a path through a file', '/index.html/app.js'],
    ['a link', '/assets/link.js'],
    ['a traversal', '/../secret.js'],
    ['an encoded traversal', '/%2e%2e/secret.js'],
    ['a deep encoded traversal', '/assets/%2E%2E/%2e%2e/secret.js'],
    ['an encoded slash', '/..%2fsecret.js'],
    ['a backslash', '/..%5csecret.js'],
    ['an absolute path', `/${join(outer, 'secret.js')}`],
    ['an encoded absolute path', `/${encodeURIComponent(join(outer, 'secret.js'))}`],
    ['a NUL byte', '/assets/app.js%00.html'],
    ['a malformed escape', '/assets/%E0%A4%A.js'],
  ])('answers 404 for %s', async (_label, path) => {
    const reply = await get(path);
    expect(reply.status).toBe(404);
    expect(reply.body).toBe('Not found');
  });

  it('answers HEAD without a body and refuses other methods', async () => {
    const head = await get('/assets/app.js', 'HEAD');
    expect(head).toMatchObject({ status: 200, body: '' });
    expect(head.headers['content-length']).toBe(String('/* app.js */'.length));
    const post = await get('/assets/app.js', 'POST');
    expect(post).toMatchObject({ status: 405, headers: { allow: 'GET, HEAD' } });
  });
});

describe('resolveRequestPath', () => {
  it('refuses a request target that is not origin-form', () => {
    expect(resolveRequestPath(root, 'http://example.com/index.html')).toBeUndefined();
    expect(resolveRequestPath(root, '*')).toBeUndefined();
    expect(resolveRequestPath(root, '/#frag')).toBe(join(root, 'index.html'));
  });
});

describe('the command line', () => {
  it('parses the folder and the port', () => {
    expect(parseHostArgs(['dist/artifact'])).toEqual({ dir: 'dist/artifact', port: DEFAULT_PORT });
    expect(parseHostArgs(['dist/artifact', '--port', '0'])).toEqual({ dir: 'dist/artifact', port: 0 });
    expect(() => parseHostArgs([])).toThrow(/^Usage/);
    expect(() => parseHostArgs(['a', 'b'])).toThrow(/^Usage/);
    expect(() => parseHostArgs(['a', '--port', '70000'])).toThrow(/Invalid --port: 70000/);
    expect(() => parseHostArgs(['a', '--port', '12ab'])).toThrow(/Invalid --port/);
  });

  it('refuses a folder without a page, and serves one with a page', async () => {
    expect(() => main([outer, '--port', '0'])).toThrow(/No index\.html/);
    const log = vi.spyOn(console, 'log').mockImplementation(() => undefined);
    const host = main([root, '--port', '0']);
    const started = await listening(host);
    host.close();
    expect(log).toHaveBeenCalledWith(`Artifact host: http://127.0.0.1:${started}/ serving ${root}`);
    log.mockRestore();
  });
});
