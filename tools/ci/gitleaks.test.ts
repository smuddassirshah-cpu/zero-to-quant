import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';
import {
  BUILD_INFO,
  EXPECTED_RULES,
  binaryCandidates,
  installEnv,
  main,
  plantedFile,
  resolveBinary,
  ruleIds,
  scanArgs,
  type Deps,
} from './gitleaks.ts';
import { run, type Run } from './proc.ts';

const dirs: string[] = [];
afterEach(() => {
  for (const dir of dirs.splice(0)) rmSync(dir, { recursive: true, force: true });
});

/** A repository root with a fake binary that carries the pinned build info, and the example env files. */
function fakeRoot(binary: Buffer | null = Buffer.concat([Buffer.from('ELF'), BUILD_INFO])): string {
  const root = mkdtempSync(join(tmpdir(), 'zq-gitleaks-test-'));
  dirs.push(root);
  if (binary !== null) {
    mkdirSync(join(root, '.zq', 'bin'), { recursive: true });
    writeFileSync(join(root, '.zq', 'bin', 'gitleaks'), binary);
  }
  for (const name of ['.env.example', '.env.eval.example', '.dev.vars.example']) {
    writeFileSync(join(root, name), 'MODEL=replace-with-a-model\n');
  }
  return root;
}

function deps(root: string, fake: Run, env: NodeJS.ProcessEnv = process.env) {
  const lines: string[] = [];
  const d: Deps = { root, env, run: fake, log: (line) => lines.push(line) };
  return { d, lines };
}

const result = (code: number) => ({ code, stdout: '', stderr: '', missing: false });

describe('install', () => {
  it('uses only the module proxy and the checksum database, into .zq/bin', () => {
    const env = installEnv('/repo', { GOPROXY: 'direct', GOSUMDB: 'off', HOME: '/home/x' });
    expect(env).toMatchObject({ GOBIN: join('/repo', '.zq', 'bin'), GOPROXY: 'https://proxy.golang.org' });
    expect(env).toMatchObject({ GOSUMDB: 'sum.golang.org', GOTOOLCHAIN: 'auto', HOME: '/home/x' });
  });

  it('fails clearly without go', async () => {
    const { d, lines } = deps(fakeRoot(null), () => Promise.resolve({ ...result(127), missing: true }));
    expect(await main(['install'], d)).toBe(1);
    expect(lines.join('\n')).toMatch(/go is not installed/);
  });

  it('passes on a go failure and checks the built binary', async () => {
    const root = fakeRoot();
    expect(await main(['install'], deps(root, () => Promise.resolve(result(2))).d)).toBe(2);
    const { d, lines } = deps(root, () => Promise.resolve(result(0)));
    expect(await main(['install'], d)).toBe(0);
    expect(lines).toEqual([`gitleaks v8.30.1 installed at ${join(root, '.zq', 'bin', 'gitleaks')}`]);
  });
});

describe('binary resolution', () => {
  it('prefers .zq/bin, then PATH in order', () => {
    expect(binaryCandidates('/r', '/a:/b')).toEqual(['/r/.zq/bin/gitleaks', '/a/gitleaks', '/b/gitleaks']);
    expect(binaryCandidates('/r', 'C:\\x;', true)).toEqual(['/r/.zq/bin/gitleaks.exe', 'C:\\x/gitleaks.exe']);
  });

  it('requires an installed binary built from the pinned module', () => {
    const root = fakeRoot(Buffer.from('another build'));
    const candidates = binaryCandidates(root);
    expect(() => resolveBinary([join(root, 'none')])).toThrow(/run npm run setup:gitleaks/);
    expect(() => resolveBinary(candidates)).toThrow(/is not gitleaks v8.30.1/);
    writeFileSync(candidates[0] ?? '', BUILD_INFO);
    expect(resolveBinary(candidates)).toBe(candidates[0]);
  });
});

describe('scans', () => {
  it('builds the redacted staged and full-history arguments', () => {
    const common = ['--redact', '--config', 'c.toml', '--no-banner', '--ignore-gitleaks-allow'];
    expect(scanArgs('staged', 'c.toml')).toEqual(['git', '--pre-commit', '--staged', ...common]);
    expect(scanArgs('history', 'c.toml', 'r.json')).toEqual([
      'git',
      ...common,
      ...['--report-format', 'json', '--report-path', 'r.json', '--log-opts=--all', '.'],
    ]);
  });

  it('runs the resolved binary and returns its exit code', async () => {
    const root = fakeRoot();
    const calls: string[][] = [];
    const fake: Run = (cmd, args) => (calls.push([cmd, ...args]), Promise.resolve(result(1)));
    expect(await main(['history'], deps(root, fake).d)).toBe(1);
    expect(calls[0]?.slice(0, 2)).toEqual([join(root, '.zq', 'bin', 'gitleaks'), 'git']);
  });

  it('refuses a .gitleaksignore file and an unknown command', async () => {
    const root = fakeRoot();
    writeFileSync(join(root, '.gitleaksignore'), 'fingerprint\n');
    const { d, lines } = deps(root, () => Promise.resolve(result(0)));
    expect(await main(['staged'], d)).toBe(1);
    expect(await main(['scan'], d)).toBe(2);
    expect(lines[0]).toMatch(/remove .gitleaksignore/);
  });
});

describe('selftest', () => {
  it('plants an Anthropic key and both proxy secrets from random bytes', () => {
    const lines = plantedFile((n) => Buffer.alloc(n, 0xfb)).split('\n');
    const prefix = ['sk', 'ant', 'api03'].join('-');
    expect(lines[0]).toMatch(new RegExp(`^ANTHROPIC_API_KEY=${prefix}-[\\w-]{93}AA$`));
    expect(lines[1]).toMatch(/^TUTOR_TOKEN=[\w-]{43}$/);
    expect(lines[2]).toMatch(/^CALL_SIGNING_KEY=[\w-]{43}$/);
    expect(plantedFile()).not.toBe(plantedFile());
  });

  it('reads rule ids from a report', () => {
    expect(ruleIds('[{"RuleID":"b"},{"RuleID":"a"},{"RuleID":"b"},{}]')).toEqual(['?', 'a', 'b']);
    expect(() => ruleIds('{}')).toThrow(/not a JSON array/);
  });

  // Real git builds the repositories; a stand-in for gitleaks reports by repository name.
  const withFake = (planted: string[], plantedCode: number, cleanCode: number): Run => {
    return (cmd, args, options) => {
      if (cmd === 'git') return run(cmd, args, options);
      const report = args[args.indexOf('--report-path') + 1] ?? '';
      const isPlanted = options?.cwd?.includes('planted') === true;
      const rules = isPlanted ? planted : [];
      writeFileSync(report, JSON.stringify(rules.map((RuleID) => ({ RuleID }))));
      return Promise.resolve(result(isPlanted ? plantedCode : cleanCode));
    };
  };

  it('passes when the planted repository fails with every rule and the clean one passes', async () => {
    const { d, lines } = deps(fakeRoot(), withFake(EXPECTED_RULES, 1, 0));
    expect(await main(['selftest'], d)).toBe(0);
    expect(lines).toEqual([
      `gitleaks selftest: planted staged scan exited 1 with ${EXPECTED_RULES.join(', ')}`,
      `gitleaks selftest: planted history scan exited 1 with ${EXPECTED_RULES.join(', ')}`,
      'gitleaks selftest: clean staged and history scans of the example env files and the older dummies exited 0',
    ]);
  });

  it('fails on a wrong exit code, a missed rule or a failing clean repository', async () => {
    const { d, lines } = deps(fakeRoot(), withFake(['zq-tutor-token'], 0, 1));
    expect(await main(['selftest'], d)).toBe(1);
    const missed = 'missed anthropic-api-key, zq-call-signing-key';
    expect(lines).toEqual([
      'gitleaks selftest: planted staged scan exited 0, expected 1',
      `gitleaks selftest: planted staged scan ${missed}`,
      'gitleaks selftest: planted history scan exited 0, expected 1',
      `gitleaks selftest: planted history scan ${missed}`,
      'gitleaks selftest: clean staged scan exited 1 (no findings)',
      'gitleaks selftest: clean history scan exited 1 (no findings)',
    ]);
  });

  it('fails when gitleaks itself errors', async () => {
    const fake: Run = (cmd, args, options) =>
      cmd === 'git' ? run(cmd, args, options) : Promise.resolve({ ...result(2), stderr: 'bad config' });
    const { d, lines } = deps(fakeRoot(), fake);
    expect(await main(['selftest'], d)).toBe(1);
    expect(lines).toEqual(['gitleaks: gitleaks failed (exit 2): bad config']);
  });
});
