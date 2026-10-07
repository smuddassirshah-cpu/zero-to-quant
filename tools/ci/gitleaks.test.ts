import { spawnSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { devNull, tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';
import {
  BUILD_INFO,
  CASES,
  EXPECTED_RULES,
  binaryCandidates,
  errorLine,
  gitEnv,
  hiddenPaths,
  hidesDiffs,
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
    writeFileSync(join(root, name), 'MODEL=replace-me\n');
  }
  return root;
}

const identity = { GIT_CONFIG_GLOBAL: devNull, GIT_CONFIG_NOSYSTEM: '1' };

function deps(root: string, fake: Run, env: NodeJS.ProcessEnv = { ...process.env, ...identity }) {
  const lines: string[] = [];
  const d: Deps = { root, env, run: fake, log: (line) => lines.push(line) };
  return { d, lines };
}

const result = (code: number, stderr = '') => ({ code, stdout: '', stderr, missing: false });

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

describe('scan inputs', () => {
  it('builds the redacted staged and full-history arguments', () => {
    const common = ['--redact', '--config', 'c.toml', '--no-banner', '--no-color', '--ignore-gitleaks-allow'];
    expect(scanArgs('staged', 'c.toml')).toEqual(['git', '--pre-commit', '--staged', ...common]);
    expect(scanArgs('history', 'c.toml', 'r.json')).toEqual([
      'git',
      ...common,
      ...['--report-format', 'json', '--report-path', 'r.json'],
      '--log-opts=--all --diff-merges=remerge --text --no-textconv --no-ext-diff',
      '.',
    ]);
  });

  it('fixes the diff format and drops config the developer could pass down', () => {
    const env = gitEnv({
      HOME: '/h',
      GIT_INDEX_FILE: 'i',
      GIT_CONFIG_PARAMETERS: "'color.ui'='always'",
      GIT_CONFIG_COUNT: '9',
      GIT_CONFIG_KEY_8: 'x',
      GIT_EXTERNAL_DIFF: 'cat',
    });
    expect(env).toMatchObject({ HOME: '/h', GIT_INDEX_FILE: 'i', GIT_CONFIG_COUNT: '8' });
    expect(env).toMatchObject({ GIT_CONFIG_KEY_0: 'color.ui', GIT_CONFIG_VALUE_0: 'never' });
    expect(env).toMatchObject({ GIT_CONFIG_KEY_7: 'diff.external', GIT_CONFIG_VALUE_7: '' });
    for (const k of ['GIT_CONFIG_PARAMETERS', 'GIT_CONFIG_KEY_8', 'GIT_EXTERNAL_DIFF'])
      expect(env[k]).toBeUndefined();
  });

  it('finds paths and attribute files that hide diffs', () => {
    const out = 'a.txt diff unset b.md diff unspecified c.cfg diff hide d diff set'.split(' ');
    expect(hiddenPaths(`${out.join('\0')}\0`)).toEqual(['a.txt', 'c.cfg']);
    for (const text of ['x -diff', '*.conf binary', '[attr]bin2 -diff -merge', 'y diff=hide eol=lf']) {
      expect(hidesDiffs(text)).toBe(true);
    }
    for (const text of ['*.sh text eol=lf', 'z !diff', 'linguist-diff=false'])
      expect(hidesDiffs(text)).toBe(false);
  });

  it('spots the ERR line gitleaks logs when git fails', () => {
    expect(errorLine('1:23PM INF 0 commits scanned.\n1:23PM ERR [git] fatal: bad\n')).toBe(
      '1:23PM ERR [git] fatal: bad',
    );
    expect(errorLine('1:23PM WRN leaks found: 1\n')).toBeUndefined();
  });
});

describe('scans of this repository', () => {
  it('runs the resolved binary, logs its output and returns its exit code', async () => {
    const root = fakeRoot();
    const calls: string[][] = [];
    const fake: Run = (cmd, args) => {
      calls.push([cmd, ...args]);
      return Promise.resolve({ ...result(1, '1:00PM INF 3 commits scanned.\n'), stdout: 'finding' });
    };
    const { d, lines } = deps(root, fake);
    expect(await main(['history'], d)).toBe(1);
    expect(calls[0]?.slice(0, 2)).toEqual([join(root, '.zq', 'bin', 'gitleaks'), 'git']);
    expect(lines).toEqual(['finding1:00PM INF 3 commits scanned.']);
  });

  it('fails a scan gitleaks passed while git failed, or of no commits', async () => {
    const err: Run = () =>
      Promise.resolve(result(0, '1:00PM ERR [git] fatal: bad\n1:00PM INF no leaks found\n'));
    const a = deps(fakeRoot(), err);
    expect(await main(['history'], a.d)).toBe(2);
    expect(a.lines.at(-1)).toBe(
      'gitleaks: history scan refused: gitleaks failed: 1:00PM ERR [git] fatal: bad',
    );
    const none: Run = (cmd) =>
      Promise.resolve(
        cmd === 'git' ? { ...result(0), stdout: 'abc\n' } : result(0, '1:00PM INF 0 commits scanned.\n'),
      );
    const b = deps(fakeRoot(), none);
    expect(await main(['history'], b.d)).toBe(2);
    expect(b.lines.at(-1)).toMatch(/scanned no commits of a repository that has some/);
  });

  it('refuses a staged scan that git would show no diff for, before running gitleaks', async () => {
    const root = fakeRoot();
    const env = { ...process.env, ...identity };
    const who = ['-c', 'user.name=t', '-c', 'user.email=t@invalid', '-c', 'commit.gpgsign=false'];
    const git = (...args: string[]) => spawnSync('git', [...who, ...args], { cwd: root, env });
    git('init', '-q');
    writeFileSync(join(root, '.gitattributes'), 'secret.txt -diff\n');
    git('add', '.gitattributes');
    git('commit', '-q', '-m', 'attributes');
    writeFileSync(join(root, 'secret.txt'), 'hidden\n');
    git('add', 'secret.txt');
    const calls: string[] = [];
    const fake: Run = (cmd, args, options) => (calls.push(cmd), run(cmd, args, options));
    const { d, lines } = deps(root, fake, env);
    expect(await main(['staged'], d)).toBe(1);
    expect(lines.at(-1)).toMatch(/refused: git shows no diff for secret.txt/);
    expect(calls.every((cmd) => cmd === 'git')).toBe(true);
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
  it('plants Anthropic keys, with and without a delimiter, and both proxy secrets', () => {
    const lines = plantedFile((n) => Buffer.alloc(n, 0xfb)).split('\n');
    const prefix = ['sk', 'ant', 'api03'].join('-');
    expect(lines[0]).toMatch(new RegExp(`^ANTHROPIC_API_KEY=${prefix}-[\\w-]{93}AA$`));
    expect(lines[1]).toMatch(new RegExp(`^const k = '${prefix}-[\\w-]{93}AAz';$`));
    expect(lines[2]).toMatch(/^TUTOR_TOKEN=[\w-]{43}$/);
    expect(lines[3]).toMatch(/^CALL_SIGNING_KEY=[\w-]{43}$/);
    expect(plantedFile()).not.toBe(plantedFile());
  });

  it('reads rule ids from a report', () => {
    expect(ruleIds('[{"RuleID":"b"},{"RuleID":"a"},{"RuleID":"b"},{}]')).toEqual(['?', 'a', 'b']);
    expect(() => ruleIds('{}')).toThrow(/not a JSON array/);
  });

  // Real git builds the repositories; a stand-in for gitleaks answers by case number and mode.
  type Answer = (expect: readonly string[], mode: 'staged' | 'history') => { code: number; stderr?: string };
  const withFake = (answer: Answer, rules = true): Run => {
    return (cmd, args, options) => {
      if (cmd === 'git') return run(cmd, args, options);
      const mode = args.includes('--staged') ? 'staged' : 'history';
      const expected = CASES[Number(/-(\d+)$/.exec(options?.cwd ?? '')?.[1])]?.[mode];
      const found = expected === undefined || expected === 'refused' || !rules ? [] : expected;
      writeFileSync(
        args[args.indexOf('--report-path') + 1] ?? '',
        JSON.stringify(found.map((RuleID) => ({ RuleID }))),
      );
      const { code, stderr = '1:00PM INF 2 commits scanned.\n' } = answer(found, mode);
      return Promise.resolve(result(code, stderr));
    };
  };

  // Each selftest builds 14 real repositories, so it gets more than the default 5 s on a loaded machine.
  const SLOW = 30_000;

  it(
    'passes when every plant is caught or refused and the clean repository passes',
    async () => {
      const honest = withFake((found) => ({ code: found.length > 0 ? 1 : 0 }));
      const { d, lines } = deps(fakeRoot(), honest);
      expect(await main(['selftest'], d)).toBe(0);
      expect(lines).toHaveLength(2);
      expect(lines[1]).toMatch(
        /^gitleaks selftest, hostile git config: plain file, evil merge, .* clean passed$/,
      );
    },
    SLOW,
  );

  it(
    'fails a scan that misses and a clean repository that fails',
    async () => {
      const lazy = deps(
        fakeRoot(),
        withFake(() => ({ code: 0 }), false),
      );
      expect(await main(['selftest'], lazy.d)).toBe(1);
      expect(lazy.lines).toContain(
        'gitleaks selftest: empty git config, plain file: staged scan exited 0, expected 1',
      );
      expect(lazy.lines).toContain(
        'gitleaks selftest: empty git config, evil merge: history scan missed zq-tutor-token',
      );
      const noisy = deps(
        fakeRoot(),
        withFake(() => ({ code: 1 })),
      );
      expect(await main(['selftest'], noisy.d)).toBe(1);
      expect(noisy.lines).toContain('gitleaks selftest: hostile git config, clean: history scan exited 1');
    },
    SLOW,
  );

  it(
    'fails when gitleaks logs a git error',
    async () => {
      const errLog = withFake(() => ({ code: 0, stderr: '1:00PM ERR [git] fatal: x\n' }));
      const broken = deps(fakeRoot(), errLog);
      expect(await main(['selftest'], broken.d)).toBe(1);
      expect(broken.lines[0]).toBe(
        'gitleaks selftest: empty git config, plain file: staged scan: gitleaks failed: 1:00PM ERR [git] fatal: x',
      );
      expect(EXPECTED_RULES).toContain('zq-anthropic-key');
    },
    SLOW,
  );
});
