/*
 * Secret scanning with gitleaks, pinned (docs/PLAN.md 7.1, 7.6). Usage: node tools/ci/gitleaks.ts <command>
 *   install   go install of the pinned module into .zq/bin. Only the Go module proxy is used (no `direct`
 *             fallback to the source host) and Go's checksum database, sum.golang.org, verifies the module and
 *             any toolchain it fetches; the built binary must then carry the pinned version and module hash.
 *   staged    the pre-commit scan of the index.
 *   history   every commit of every ref, merge resolutions included (--diff-merges=remerge), every file as
 *             text with no textconv or external diff, so .gitattributes cannot hide a file.
 *   selftest  builds throwaway repositories for each way a key can be planted (a plain file, an evil merge,
 *             a -diff or binary attribute, a textconv driver) and requires both scans to catch or refuse each,
 *             and a clean repository to pass; once under an empty git config and once under a hostile one.
 *             Key-shaped values are assembled at run time, so none sits in this repository.
 * The staged scan cannot read a file whose diff attribute is unset or names a driver (git diff shows no text
 * for it), so it refuses one, and a staged .gitattributes that sets such an attribute. A file git detects as
 * binary by its content is out of the staged scan's reach; the history scan, run before every push and in
 * CI, reads it as text.
 * Every git and gitleaks child runs with command-scope config that fixes the diff format, because colour or
 * prefix settings in the developer's own config make gitleaks see nothing [measured]. gitleaks exits 0 when git
 * itself fails, logging an ERR line [measured], so any ERR line, or a history scan of no commits, fails the run.
 * Scans are redacted and ignore `gitleaks:allow` comments, and a .gitleaksignore file stops them: the only
 * allowlist is the reviewed .gitleaks.toml. Binary resolution is .zq/bin, then PATH, and whichever is found must
 * be the pinned build, or the run stops.
 */
import { randomBytes } from 'node:crypto';
import {
  copyFileSync,
  existsSync,
  mkdirSync,
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
export const EXPECTED_RULES = [
  'anthropic-api-key',
  'zq-anthropic-key',
  'zq-call-signing-key',
  'zq-tutor-token',
];
// The example env files' dummy values at cf706c4 that match the proxy secret rules, allowlisted exactly.
const HISTORY_DUMMIES = [
  ['replace', 'with', '43', 'or', 'more', 'base64url', 'characters'],
  ['replace', 'with', '32', 'random', 'bytes', 'base64url'],
  ['replace', 'with', 'an', 'eval', 'only', 'signing', 'key'],
].map((words) => words.join('-'));
// Each `key=value`; diff.external is set empty. color.diff outranks color.ui, so both are needed [measured].
const GIT_OVERRIDES = ['color.ui=never', 'color.diff=never', 'core.quotepath=false', 'diff.noprefix=false']
  .concat(['diff.mnemonicprefix=false', 'diff.srcPrefix=a/', 'diff.dstPrefix=b/', 'diff.external='])
  .map((pair) => pair.split('='));
const HISTORY_LOG = '--all --diff-merges=remerge --text --no-textconv --no-ext-diff';

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
    ...Object.fromEntries(
      ['GONOSUMDB', 'GONOPROXY', 'GOPRIVATE', 'GOINSECURE', 'GOFLAGS'].map((k) => [k, '']),
    ),
    // gitleaks v8.30.1 declares go 1.24.11; an older local Go fetches a newer toolchain, verified like a module.
    GOTOOLCHAIN: 'auto',
  };
}

/** The environment of every git and gitleaks child: command-scope config wins over every config file. */
export function gitEnv(env: NodeJS.ProcessEnv): NodeJS.ProcessEnv {
  // GIT_CONFIG_PARAMETERS (`git -c`, passed down to hooks) would win over GIT_CONFIG_COUNT [measured]; drop it.
  const out = Object.fromEntries(
    Object.entries(env).filter(
      ([k]) => !/^GIT_(CONFIG_(COUNT|KEY_\d+|VALUE_\d+|PARAMETERS)|EXTERNAL_DIFF)$/.test(k),
    ),
  );
  GIT_OVERRIDES.forEach(([key = '', value = ''], i) => {
    out[`GIT_CONFIG_KEY_${i}`] = key;
    out[`GIT_CONFIG_VALUE_${i}`] = value;
  });
  return { ...out, GIT_CONFIG_COUNT: String(GIT_OVERRIDES.length) };
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
  const common = ['--redact', '--config', config, '--no-banner', '--no-color', '--ignore-gitleaks-allow'];
  if (report !== undefined) common.push('--report-format', 'json', '--report-path', report);
  return mode === 'staged'
    ? ['git', '--pre-commit', '--staged', ...common]
    : ['git', ...common, `--log-opts=${HISTORY_LOG}`, '.'];
}

/** Paths from `git check-attr -z diff` output whose diff is unset (-diff, binary) or names a driver. */
export function hiddenPaths(checkAttr: string): string[] {
  const fields = checkAttr.split('\0');
  const hidden: string[] = [];
  for (let i = 0; i + 2 < fields.length; i += 3) {
    if (fields[i + 2] !== 'unspecified' && fields[i + 2] !== 'set') hidden.push(fields[i] ?? '');
  }
  return hidden;
}

/** Whether .gitattributes text sets -diff, binary or a diff driver, directly or in a macro. */
export const hidesDiffs = (text: string): boolean => /(?:^|\s)(?:-diff|binary|diff=\S*)(?=\s|$)/m.test(text);

/** The first ERR or FTL line of gitleaks' log; gitleaks exits 0 when git fails [measured]. */
export const errorLine = (stderr: string): string | undefined =>
  stderr.split('\n').find((line) => /\s(?:ERR|FTL)\s/.test(line));

/** The file planted by the selftest: Anthropic keys and both proxy secrets, each from fresh random bytes. */
export function plantedFile(random: (size: number) => Buffer = randomBytes): string {
  const b64 = (size: number) => random(size).toString('base64url');
  const key = () => ['sk', 'ant', 'api03', b64(70).slice(0, 93)].join('-') + 'AA';
  return [
    `ANTHROPIC_API_KEY=${key()}`,
    // No delimiter after the key, which the default anthropic-api-key rule needs: only zq-anthropic-key sees it.
    `const k = '${key()}z';`,
    `TUTOR_TOKEN=${b64(32)}`,
    `CALL_SIGNING_KEY=${b64(32)}`,
    '',
  ].join('\n');
}

export function ruleIds(report: string): string[] {
  const findings: unknown = JSON.parse(report);
  if (!Array.isArray(findings)) throw new Error('gitleaks report is not a JSON array');
  const ids = findings.map((f: unknown) =>
    typeof f === 'object' && f !== null && 'RuleID' in f && typeof f.RuleID === 'string' ? f.RuleID : '?',
  );
  return [...new Set(ids)].sort();
}

interface Scan {
  readonly code: number;
  readonly rules: readonly string[];
  /** Why the scan refused or failed, when it did not report leaks itself. */
  readonly problem?: string;
  readonly output: string;
}

/** One scan of `dir`: the staged refusals, then gitleaks, failing on any ERR line or an empty history. */
async function scanRepo(deps: Deps, bin: string, dir: string, mode: 'staged' | 'history', report?: string) {
  const env = gitEnv(deps.env);
  const git = async (args: string[], input?: string) => {
    const r = await deps.run('git', args, { cwd: dir, env, capture: true, input });
    if (r.code !== 0) throw new Error(`git ${args[0] ?? ''} failed: ${r.stderr.trim()}`);
    return r.stdout;
  };
  const refuse = (problem: string): Scan => ({ code: 1, rules: [], problem, output: '' });
  if (mode === 'staged') {
    const index = await git(['ls-files', '-z']);
    const hidden = hiddenPaths(await git(['check-attr', '--cached', '-z', '--stdin', 'diff'], index));
    if (hidden.length > 0)
      return refuse(`git shows no diff for ${hidden.join(', ')}: drop its diff attribute`);
    const staged = (await git(['diff', '--cached', '--name-only', '-z', '--diff-filter=ACMR'])).split('\0');
    for (const path of staged.filter((p) => /(?:^|\/)\.gitattributes$/.test(p))) {
      const text = await git(['show', `:${path}`]);
      if (hidesDiffs(text)) return refuse(`${path} sets -diff, binary or a diff driver, which hides diffs`);
    }
  }
  const config = join(deps.root, '.gitleaks.toml');
  const r = await deps.run(bin, scanArgs(mode, config, report), { cwd: dir, env, capture: true });
  const output = r.stdout + r.stderr;
  let rules: string[] = [];
  if (report !== undefined && existsSync(report)) {
    rules = ruleIds(readFileSync(report, 'utf8'));
    rmSync(report);
  }
  const failed = errorLine(r.stderr);
  if (r.code > 1 || failed !== undefined) {
    return { code: 2, rules, problem: `gitleaks failed: ${(failed ?? r.stderr).trim()}`, output };
  }
  const none = mode === 'history' && /\b0 commits scanned/.test(r.stderr);
  if (none && (await git(['rev-list', '--all', '-n', '1'])) !== '') {
    return { code: 2, rules, problem: 'gitleaks scanned no commits of a repository that has some', output };
  }
  return { code: r.code, rules, output };
}

async function scan(deps: Deps, mode: 'staged' | 'history'): Promise<number> {
  if (existsSync(join(deps.root, '.gitleaksignore'))) {
    throw new Error('remove .gitleaksignore: allowlists belong in the reviewed .gitleaks.toml');
  }
  const bin = resolveBinary(binaryCandidates(deps.root, deps.env.PATH));
  const result = await scanRepo(deps, bin, deps.root, mode);
  for (const line of result.output.trimEnd().split('\n')) deps.log(line);
  if (result.problem !== undefined) deps.log(`gitleaks: ${mode} scan refused: ${result.problem}`);
  return result.code;
}

async function install(deps: Deps): Promise<number> {
  const result = await deps.run('go', ['install', `${MODULE}@${VERSION}`], {
    env: installEnv(deps.root, deps.env),
  });
  if (result.missing)
    throw new Error('go is not installed: install Go 1.24.11 or later, then npm run setup:gitleaks');
  if (result.code !== 0) return result.code;
  deps.log(`gitleaks ${VERSION} installed at ${resolveBinary(binaryCandidates(deps.root).slice(0, 1))}`);
  return 0;
}

/** What each selftest repository must give: the rules a scan reports (none means it passes) or a refusal. */
type Expect = readonly string[] | 'refused';
interface Case {
  readonly name: string;
  /** Writes and stages the plant; `finish` then commits it, so the history scan sees it. */
  readonly stage: (dir: string, git: (...args: string[]) => Promise<void>, root: string) => Promise<void>;
  readonly finish?: (git: (...args: string[]) => Promise<void>) => Promise<void>;
  readonly staged: Expect;
  readonly history: Expect;
}

const token = () => `TUTOR_TOKEN=${randomBytes(32).toString('base64url')}\n`;
// The attribute is committed first, so only the check of every index path refuses the staged plant.
const hiddenBy = (name: string, attributes: string, file: string): Case => ({
  name,
  stage: async (dir, git) => {
    writeFileSync(join(dir, '.gitattributes'), `${attributes}\n`);
    await git('add', '-A');
    await git('commit', '-q', '-m', 'attributes');
    writeFileSync(join(dir, file), token());
    await git('add', '-A');
  },
  // Stays on the side branch: git reads attributes from the checked-out tree, so the history scan meets them.
  finish: (git) => git('commit', '-q', '-m', name),
  staged: 'refused',
  history: ['zq-tutor-token'],
});

export const CASES: readonly Case[] = [
  {
    name: 'plain file',
    stage: async (dir, git) => {
      writeFileSync(join(dir, 'proxy.env'), plantedFile());
      await git('add', '-A');
    },
    staged: EXPECTED_RULES,
    history: EXPECTED_RULES,
  },
  {
    // A token that is in neither parent, only in the merge commit's resolution.
    name: 'evil merge',
    stage: async (dir, git) => {
      await git('commit', '-q', '--allow-empty', '-m', 'side');
      await git('switch', '-q', 'main');
      writeFileSync(join(dir, 'main.txt'), 'main\n');
      await git('add', '-A');
      await git('commit', '-q', '-m', 'main');
      await git('merge', '-q', '--no-ff', '--no-commit', 'side');
      writeFileSync(join(dir, 'README.txt'), `selftest\n${token()}`);
      await git('add', '-A');
    },
    finish: (git) => git('commit', '-q', '-m', 'merge'),
    staged: ['zq-tutor-token'],
    history: ['zq-tutor-token'],
  },
  hiddenBy('-diff attribute', 'secrets.txt -diff', 'secrets.txt'),
  hiddenBy('binary attribute', '*.conf binary', 'proxy.conf'),
  hiddenBy('textconv driver', '*.cfg diff=hide', 'proxy.cfg'),
  {
    // An attribute for files not yet added: only the check of the staged .gitattributes refuses it.
    name: 'staged .gitattributes',
    stage: async (dir, git) => {
      writeFileSync(join(dir, '.gitattributes'), '*.later -diff\n');
      await git('add', '-A');
    },
    staged: 'refused',
    history: [],
  },
  {
    // The example files hold dummy values only; the older dummies, still in history, match the proxy
    // secret rules, so only the allowlist lets them pass.
    name: 'clean',
    stage: async (dir, git, root) => {
      for (const name of ['.env.example', '.env.eval.example', '.dev.vars.example']) {
        copyFileSync(join(root, name), join(dir, name));
      }
      const dummies = HISTORY_DUMMIES.map((v, i) => `${i === 0 ? 'TUTOR_TOKEN' : 'CALL_SIGNING_KEY'}=${v}`);
      writeFileSync(join(dir, 'history.env.example'), `${dummies.join('\n')}\n`);
      await git('add', '-A');
    },
    staged: [],
    history: [],
  },
];

// Everything a developer's config could set to blind the scans; the textconv driver empties proxy.cfg.
const HOSTILE_CONFIG =
  '[color]\n ui = always\n diff = always\n[core]\n quotepath = true\n[diff]\n noprefix = true\n' +
  ' mnemonicprefix = true\n external = true\n[diff "hide"]\n textconv = true\n';

function verdict(name: string, mode: string, expect: Expect, got: Scan): string[] {
  if (expect === 'refused') {
    return got.problem !== undefined && got.code === 1 ? [] : [`${name}: ${mode} scan was not refused`];
  }
  if (got.problem !== undefined) return [`${name}: ${mode} scan: ${got.problem}`];
  if (expect.length === 0) return got.code === 0 ? [] : [`${name}: ${mode} scan exited ${got.code}`];
  const missed = expect.filter((id) => !got.rules.includes(id));
  return [
    ...(got.code === 1 ? [] : [`${name}: ${mode} scan exited ${got.code}, expected 1`]),
    ...(missed.length === 0 ? [] : [`${name}: ${mode} scan missed ${missed.join(', ')}`]),
  ];
}

async function selftest(deps: Deps): Promise<number> {
  const bin = resolveBinary(binaryCandidates(deps.root, deps.env.PATH));
  const work = mkdtempSync(join(tmpdir(), 'zq-gitleaks-selftest-'));
  const hostile = join(work, 'hostile.gitconfig');
  writeFileSync(hostile, HOSTILE_CONFIG);
  const base = { ...deps.env, GIT_CONFIG_NOSYSTEM: '1' };
  const parameters = { GIT_CONFIG_PARAMETERS: "'color.diff'='always'", GIT_EXTERNAL_DIFF: 'true' };
  const passes = [
    { label: 'empty git config', env: { ...base, GIT_CONFIG_GLOBAL: devNull } },
    { label: 'hostile git config', env: { ...base, ...parameters, GIT_CONFIG_GLOBAL: hostile } },
  ];
  const identity = [
    '-c',
    'user.name=zq selftest',
    '-c',
    'user.email=selftest@invalid',
    '-c',
    'commit.gpgsign=false',
  ];
  const failures: string[] = [];
  try {
    for (const pass of passes) {
      const scanDeps: Deps = { ...deps, env: pass.env };
      for (const [n, c] of CASES.entries()) {
        const dir = join(work, `${pass.label.split(' ')[0] ?? ''}-${n}`);
        // The repository is built under an empty config; only the scans see the hostile one.
        const buildEnv = gitEnv({ ...pass.env, GIT_CONFIG_GLOBAL: devNull });
        const git = async (...args: string[]) => {
          const r = await deps.run('git', [...identity, ...args], { cwd: dir, env: buildEnv, capture: true });
          if (r.code !== 0)
            throw new Error(`git ${args[0] ?? ''} failed in the selftest: ${r.stderr.trim()}`);
        };
        mkdirSync(dir);
        await git('init', '-q', '-b', 'main');
        writeFileSync(join(dir, 'README.txt'), 'selftest\n');
        await git('add', '-A');
        await git('commit', '-q', '-m', 'clean');
        // Each plant goes on a side branch, so only a scan of every ref can see it.
        await git('switch', '-q', '-c', 'side');
        await c.stage(dir, git, deps.root);
        const staged = await scanRepo(scanDeps, bin, dir, 'staged', `${dir}-staged.json`);
        await (c.finish ?? ((g) => g('commit', '-q', '-m', c.name)))(git);
        if (c.finish === undefined) await git('switch', '-q', 'main');
        const history = await scanRepo(scanDeps, bin, dir, 'history', `${dir}-history.json`);
        failures.push(
          ...verdict(`${pass.label}, ${c.name}`, 'staged', c.staged, staged),
          ...verdict(`${pass.label}, ${c.name}`, 'history', c.history, history),
        );
      }
    }
  } finally {
    rmSync(work, { recursive: true, force: true });
  }
  for (const failure of failures) deps.log(`gitleaks selftest: ${failure}`);
  if (failures.length > 0) return 1;
  const planted = CASES.filter((c) => c.name !== 'clean').map((c) => c.name);
  for (const { label } of passes) {
    deps.log(
      `gitleaks selftest, ${label}: ${planted.join(', ')} caught or refused as expected; clean passed`,
    );
  }
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
