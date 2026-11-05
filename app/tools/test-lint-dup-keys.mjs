#!/usr/bin/env node
/* Test for tools/lint-dup-keys.mjs (ENGINE-BACKLOG 571): the bad fixture is reported, the good one passes, the real tree is clean. */
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url));
const lint = path.join(here, 'lint-dup-keys.mjs');
let bad = 0;
const check = (name, ok, detail = '') => { console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${ok ? '' : '  ' + detail}`); if (!ok) bad++; };
const run = (f) => spawnSync('node', [lint, path.join(here, 'fixtures/lint-dup-keys', f)], { encoding: 'utf8' });
const b = run('bad.js'), g = run('good.js');
check('bad fixture exits 1', b.status === 1, String(b.status));
check('bad fixture: duplicate method key status', /duplicate key "status"/.test(b.stdout), b.stdout);
check('bad fixture: duplicate string key a-b', /duplicate key "a-b"/.test(b.stdout), b.stdout);
check('bad fixture: api.run assignment replaces the literal function', /"api\.run =" replaces the function "run"/.test(b.stdout), b.stdout);
check('bad fixture: exactly 3 findings', /3 findings/.test(b.stdout), b.stdout);
check('good fixture exits 0 with no findings', g.status === 0 && /0 findings/.test(g.stdout), g.stdout);
const tree = spawnSync('node', [lint, path.join(here, '..', 'js')], { encoding: 'utf8' });
check('app/js is clean', tree.status === 0, tree.stdout);
console.log(bad ? `${bad} failed` : 'all passed');
process.exit(bad ? 1 : 0);
