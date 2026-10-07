/*
 * Secret scanning with gitleaks, pinned (docs/PLAN.md 7.1, 7.6). Usage: node tools/ci/gitleaks.ts <command>
 *   install   go install of the pinned module into .zq/bin. Only the Go module proxy is used (no `direct`
 *             fallback to the source host) and Go's checksum database, sum.golang.org, verifies the module and
 *             any toolchain it fetches; the built binary must then carry the pinned version and module hash.
 *   staged    the pre-commit scan of the index.
 *   history   every commit of every ref.
 *   selftest  plants generated fake keys in a throwaway repository and requires the staged scan of its index
 *             and the history scan, with the plant committed on a side branch, each to fail with every expected
 *             rule id; a clean repository must pass both. Key-shaped values are assembled at run time, so none
 *             sits in this repository for the history scan to find.
 * Scans are redacted and ignore `gitleaks:allow` comments, and a .gitleaksignore file stops them: the only
 * allowlist is the reviewed .gitleaks.toml. Binary resolution is .zq/bin, then PATH, and whichever is found must
 * be the pinned build, or the run stops.
 */
import { randomBytes } from 'node:crypto';
import {
  copyFileSync,
  existsSync,
  mkdtempSync,
  readFileSync,
  rmSync,
  statSync,
  writeFileSync,
} from 'node:fs';
import { devNull, tmpdir } from 'node:os';
import { delimiter, join } from 'node:path';
import { repoRoot, run as realRun, type Log, type Run } from './proc.ts';

const MODULE = 'github.com/zricethezav/gitleaks/v8';
const VERSION = 'v8.30.1';
// [measured] `go version -m` on the binary built through sum.golang.org, 7 October 2026.
const MODULE_SUM = 'h1:PmEvCfVI7ti9dV3s5aMZUY7sS2GxRvG3yzih7E+cS3w=';
export const BUILD_INFO = Buffer.from(`mod\t${MODULE}\t${VERSION}\t${MODULE_SUM}`);
export const EXPECTED_RULES = ['anthropic-api-key', 'zq-call-signing-key', 'zq-tutor-token'];
// The form of the example files' dummy values at cf706c4: 44 base64url characters, allowlisted by value.
const HISTORY_DUMMY = ['replace', 'with', '43', 'or', 'more', 'base64url', 'characters'].join('-');

export interface Deps {
  readonly root: string;
  readonly env: NodeJS.ProcessEnv;
  readonly run: Run;
  readonly log: Log;
}

export function installEnv(root: string, env: NodeJS.ProcessEnv): NodeJS.ProcessEnv {
  return {
    ...env,
    GOBIN: join(root, '.zq', 'bin'),
    GOPROXY: 'https://proxy.golang.org',
    GOSUMDB: 'sum.golang.org',
    GONOSUMDB: '',
    GONOPROXY: '',
    GOPRIVATE: '',
    GOINSECURE: '',
    GOFLAGS: '',
    // gitleaks v8.30.1 declares go 1.24.11; an older local Go fetches a newer toolchain, verified like a module.
    GOTOOLCHAIN: 'auto',
  };
}

export function binaryCandidates(
  root: string,
  pathEnv = '',
  windows = process.platform === 'win32',
): string[] {
  const exe = windows ? 'gitleaks.exe' : 'gitleaks';
  const dirs = pathEnv.split(windows ? ';' : delimiter).filter((dir) => dir !== '');
  return [join(root, '.zq', 'bin', exe), ...dirs.map((dir) => join(dir, exe))];
}

const isFile = (path: string): boolean => existsSync(path) && statSync(path).isFile();

/** The first candidate that exists; an error naming the fix when none does or it is not the pinned build. */
export function resolveBinary(candidates: readonly string[]): string {
  const found = candidates.find(isFile);
  if (found === undefined) throw new Error('gitleaks is not installed: run npm run setup:gitleaks');
  if (!readFileSync(found).includes(BUILD_INFO)) {
    throw new Error(
      `${found} is not gitleaks ${VERSION} built from the pinned module: run npm run setup:gitleaks`,
    );
  }
  return found;
}

export function scanArgs(mode: 'staged' | 'history', config: string, report?: string): string[] {
  const common = ['--redact', '--config', config, '--no-banner', '--ignore-gitleaks-allow'];
  if (report !== undefined) common.push('--report-format', 'json', '--report-path', report);
  return mode === 'staged'
    ? ['git', '--pre-commit', '--staged', ...common]
    : ['git', ...common, '--log-opts=--all', '.'];
}

/** The file planted by the selftest: an Anthropic key and both proxy secrets, each from fresh random bytes. */
export function plantedFile(random: (size: number) => Buffer = randomBytes): string {
  const b64 = (size: number) => random(size).toString('base64url');
  const anthropic = ['sk', 'ant', 'api03', b64(70).slice(0, 93)].join('-') + 'AA';
  return [`ANTHROPIC_API_KEY=${anthropic}`, `TUTOR_TOKEN=${b64(32)}`, `CALL_SIGNING_KEY=${b64(32)}`, ''].join(
    '\n',
  );
}

export function ruleIds(report: string): string[] {
  const findings: unknown = JSON.parse(report);
  if (!Array.isArray(findings)) throw new Error('gitleaks report is not a JSON array');
  const ids = findings.map((f: unknown) =>
    typeof f === 'object' && f !== null && 'RuleID' in f && typeof f.RuleID === 'string' ? f.RuleID : '?',
  );
  return [...new Set(ids)].sort();
}

async function scan(deps: Deps, mode: 'staged' | 'history'): Promise<number> {
  if (existsSync(join(deps.root, '.gitleaksignore'))) {
    throw new Error('remove .gitleaksignore: allowlists belong in the reviewed .gitleaks.toml');
  }
  const bin = resolveBinary(binaryCandidates(deps.root, deps.env.PATH));
  return (await deps.run(bin, scanArgs(mode, join(deps.root, '.gitleaks.toml')), { cwd: deps.root })).code;
}

async function install(deps: Deps): Promise<number> {
  const result = await deps.run('go', ['install', `${MODULE}@${VERSION}`], {
    env: installEnv(deps.root, deps.env),
  });
  if (result.missing)
    throw new Error('go is not installed: install Go 1.24 or later, then npm run setup:gitleaks');
  if (result.code !== 0) return result.code;
  deps.log(`gitleaks ${VERSION} installed at ${resolveBinary(binaryCandidates(deps.root).slice(0, 1))}`);
  return 0;
}

async function selftest(deps: Deps): Promise<number> {
  const bin = resolveBinary(binaryCandidates(deps.root, deps.env.PATH));
  const env: NodeJS.ProcessEnv = {
    ...deps.env,
    GIT_CONFIG_GLOBAL: devNull,
    GIT_CONFIG_NOSYSTEM: '1',
    GIT_AUTHOR_NAME: 'zq selftest',
    GIT_AUTHOR_EMAIL: 'selftest@invalid',
    GIT_COMMITTER_NAME: 'zq selftest',
    GIT_COMMITTER_EMAIL: 'selftest@invalid',
  };
  const git = async (cwd: string, ...args: string[]) => {
    const r = await deps.run('git', ['-c', 'commit.gpgsign=false', ...args], { cwd, env, capture: true });
    if (r.code !== 0) throw new Error(`git ${args[0] ?? ''} failed in the selftest: ${r.stderr.trim()}`);
  };
  const scanOnce = async (dir: string, mode: 'staged' | 'history') => {
    const report = join(dir, `${mode}.json`);
    const args = scanArgs(mode, join(deps.root, '.gitleaks.toml'), report);
    const { code, stderr } = await deps.run(bin, args, { cwd: dir, env, capture: true });
    if (code > 1 || !existsSync(report)) throw new Error(`gitleaks failed (exit ${code}): ${stderr.trim()}`);
    const rules = ruleIds(readFileSync(report, 'utf8'));
    rmSync(report);
    return { mode, code, rules };
  };
  // Each repository is scanned twice: its index, as the pre-commit hook does, then every ref once committed.
  const repository = async (kind: string, plant: (dir: string) => void) => {
    const dir = mkdtempSync(join(tmpdir(), `zq-gitleaks-${kind}-`));
    try {
      await git(dir, 'init', '-q', '-b', 'main');
      writeFileSync(join(dir, 'README.txt'), 'selftest\n');
      await git(dir, 'add', '-A');
      await git(dir, 'commit', '-q', '-m', 'clean');
      // The plant goes on a side branch, so only a scan of every ref (--log-opts=--all) can see it.
      await git(dir, 'switch', '-q', '-c', 'side');
      plant(dir);
      await git(dir, 'add', '-A');
      const staged = await scanOnce(dir, 'staged');
      await git(dir, 'commit', '-q', '-m', kind);
      await git(dir, 'switch', '-q', 'main');
      return [staged, await scanOnce(dir, 'history')];
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  };
  const planted = await repository('planted', (dir) => {
    writeFileSync(join(dir, 'proxy.env'), plantedFile());
  });
  // The example env files hold dummy values only. The older dummies, still in history, match the proxy
  // secret rules, so the clean repository carries them too: only the allowlist lets them pass.
  const clean = await repository('clean', (dir) => {
    for (const name of ['.env.example', '.env.eval.example', '.dev.vars.example']) {
      copyFileSync(join(deps.root, name), join(dir, name));
    }
    writeFileSync(
      join(dir, 'history.env.example'),
      `TUTOR_TOKEN=${HISTORY_DUMMY}\nCALL_SIGNING_KEY=${HISTORY_DUMMY}\n`,
    );
  });
  const failures = [
    ...planted.flatMap(({ mode, code, rules }) => {
      const missed = EXPECTED_RULES.filter((id) => !rules.includes(id));
      return [
        ...(code === 1 ? [] : [`planted ${mode} scan exited ${code}, expected 1`]),
        ...(missed.length === 0 ? [] : [`planted ${mode} scan missed ${missed.join(', ')}`]),
      ];
    }),
    ...clean.flatMap(({ mode, code, rules }) =>
      code === 0 ? [] : [`clean ${mode} scan exited ${code} (${rules.join(', ') || 'no findings'})`],
    ),
  ];
  for (const failure of failures) deps.log(`gitleaks selftest: ${failure}`);
  if (failures.length > 0) return 1;
  for (const { mode, rules } of planted) {
    deps.log(`gitleaks selftest: planted ${mode} scan exited 1 with ${rules.join(', ')}`);
  }
  deps.log(
    'gitleaks selftest: clean staged and history scans of the example env files and the older dummies exited 0',
  );
  return 0;
}

export async function main(argv: readonly string[], deps: Deps): Promise<number> {
  const command = argv[0];
  try {
    if (command === 'install') return await install(deps);
    if (command === 'staged' || command === 'history') return await scan(deps, command);
    if (command === 'selftest') return await selftest(deps);
    deps.log('usage: node tools/ci/gitleaks.ts install|staged|history|selftest');
    return 2;
  } catch (error) {
    deps.log(`gitleaks: ${error instanceof Error ? error.message : String(error)}`);
    return 1;
  }
}

if (import.meta.main) {
  const deps: Deps = { root: repoRoot, env: process.env, run: realRun, log: console.log };
  process.exitCode = await main(process.argv.slice(2), deps);
}
