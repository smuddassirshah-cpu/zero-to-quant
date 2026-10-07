import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { describe, expect, it } from 'vitest';
import { ALLOWED, check, classify, main, parseExceptions, parseSpdx, satisfies } from './licences.ts';

const ok = (text: string, kind: keyof typeof ALLOWED = 'shipped') =>
  satisfies(parseSpdx(text), ALLOWED[kind]);

describe('SPDX expressions', () => {
  it.each([
    ['MIT', true],
    ['GPL-3.0', false],
    ['(MIT OR GPL-3.0)', true],
    ['MIT AND GPL-3.0', false],
    ['Apache-2.0 WITH LLVM-exception', true],
    ['(GPL-2.0 OR (MIT AND BSD-3-Clause))', true],
    ['BlueOak-1.0.0', false],
    ['mit', false],
  ])('%s for a shipped package: %s', (text, expected) => {
    expect(ok(text)).toBe(expected);
  });

  it('allows the development extras only for development packages', () => {
    expect(ok('BlueOak-1.0.0 OR CC0-1.0', 'development')).toBe(true);
    expect(ok('MIT-0', 'development')).toBe(false);
  });

  it.each(['', '(MIT', 'MIT)', 'MIT OR', 'AND MIT', 'MIT WITH', 'MIT WITH (', 'MIT BSD-2-Clause'])(
    'rejects malformed "%s"',
    (text) => {
      expect(() => parseSpdx(text)).toThrow();
    },
  );
});

// A shipped app dependency, a development tool, a development workspace whose peer is npm-marked production,
// a shipped workspace, and a nested copy resolved before the hoisted one.
const lock = {
  packages: {
    '': {
      dependencies: { app: '1.0.0' },
      devDependencies: { tool: '1.0.0', 'lint-plugin': '0.1.0' },
    },
    'node_modules/app': { version: '1.0.0', license: 'MIT', dependencies: { dep: '^2.0.0' } },
    'node_modules/app/node_modules/dep': { version: '2.0.0', license: 'ISC' },
    'node_modules/dep': { version: '1.0.0', license: 'GPL-3.0', dev: true },
    'node_modules/tool': { version: '1.0.0', license: 'BlueOak-1.0.0', dev: true },
    'node_modules/linter': { version: '9.0.0', license: 'MIT-0', optionalDependencies: { gone: '1' } },
    'node_modules/lint-plugin': { resolved: 'packages/lint-plugin', link: true },
    'packages/lint-plugin': { version: '0.1.0', license: 'MIT', peerDependencies: { linter: '9.0.0' } },
    'node_modules/@zq/core': { resolved: 'packages/core', link: true },
    'packages/core': { version: '0.1.0', dependencies: { shared: '1' } },
    'packages/core/node_modules/shared': { version: '1.0.0', license: '(MIT OR Apache-2.0)' },
  },
};

describe('classification', () => {
  it('follows production roots and shipped workspaces, nearest node_modules first', () => {
    const classes = Object.fromEntries(classify(lock).map((p) => [p.key, p.shipped]));
    expect(classes).toEqual({
      'node_modules/app': true,
      'node_modules/app/node_modules/dep': true,
      'node_modules/dep': false,
      'node_modules/tool': false,
      'node_modules/linter': false,
      'packages/core/node_modules/shared': true,
    });
  });

  it('fails on a missing required dependency or a pre-v3 lockfile', () => {
    const broken = {
      packages: { '': { dependencies: { app: '1' } }, 'node_modules/app': { dependencies: { x: '1' } } },
    };
    expect(() => classify(broken)).toThrow(/depends on x/);
    expect(() => classify({})).toThrow(/lockfile v3/);
  });
});

describe('check', () => {
  const installed = classify(lock);
  const linterException = {
    name: 'linter',
    version: '9.0.0',
    licence: 'MIT-0',
    reason: 'test',
    decision: 'docs/DECISIONS.md L0',
  };

  it('fails a licence outside the allow-list for its class, and counts per class', () => {
    const { failures, counts } = check(installed, []);
    expect(failures).toEqual([
      'dep@1.0.0 (node_modules/dep): GPL-3.0 is not allowed for development packages',
      'linter@9.0.0 (node_modules/linter): MIT-0 is not allowed for development packages',
    ]);
    expect([...counts.shipped]).toEqual([
      ['MIT', 1],
      ['ISC', 1],
      ['(MIT OR Apache-2.0)', 1],
    ]);
  });

  it('accepts a listed exception and fails a stale one', () => {
    const stale = { ...linterException, name: 'gone' };
    const { failures, excepted } = check(installed, [linterException, stale]);
    expect(excepted).toEqual([linterException]);
    expect(failures).toContain('exception gone@9.0.0 matches no failing package: remove it');
    expect(failures).toHaveLength(2);
  });

  it('fails a missing or unparsable licence', () => {
    const pkg = { key: 'node_modules/x', name: 'x', version: '1.0.0', shipped: true };
    expect(check([{ ...pkg, licence: undefined }], []).failures[0]).toMatch(/\(none\) is not allowed/);
    expect(check([{ ...pkg, licence: 'MIT OR' }], []).failures[0]).toMatch(/expected a licence/);
  });

  it('excepts a licence that is not SPDX at all, and fails it without the exception', () => {
    const licence = 'SEE LICENSE IN LICENSE.md';
    const pkg = { key: 'node_modules/x', name: 'x', version: '1.0.0', shipped: false, licence };
    const exception = {
      name: 'x',
      version: '1.0.0',
      licence,
      reason: 'read',
      decision: 'docs/DECISIONS.md L0',
    };
    expect(check([pkg], [exception])).toMatchObject({ failures: [], excepted: [exception] });
    expect(check([pkg], []).failures).toEqual([
      'x@1.0.0 (node_modules/x): unexpected "LICENSE" in "SEE LICENSE IN LICENSE.md"',
    ]);
  });

  it('validates the exceptions file', () => {
    expect(parseExceptions([linterException])).toEqual([linterException]);
    expect(() => parseExceptions({})).toThrow(/must be an array/);
    expect(() => parseExceptions([{ name: 'x' }])).toThrow(/entry 0 needs/);
  });
});

describe('main', () => {
  it('reads the lockfile and exceptions, prints counts and returns the verdict', () => {
    const root = mkdtempSync(join(tmpdir(), 'zq-licences-'));
    try {
      mkdirSync(join(root, 'tools', 'ci'), { recursive: true });
      writeFileSync(join(root, 'package-lock.json'), JSON.stringify(lock));
      writeFileSync(join(root, 'tools', 'ci', 'licences.exceptions.json'), '[]');
      const lines: string[] = [];
      expect(main(root, (line) => lines.push(line))).toBe(1);
      expect(lines[0]).toBe('licences: 3 shipped\n  (MIT OR Apache-2.0) 1\n  ISC 1\n  MIT 1');
      expect(lines.at(-1)).toMatch(/^licences: linter@9.0.0/);
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });
});
