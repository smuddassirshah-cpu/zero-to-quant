/*
 * npm audit gate (docs/PLAN.md 7.6). Usage: node tools/ci/audit.ts [--level low|moderate|high|critical]
 * - Fails on any advisory at or above the level (default high) unless tools/ci/audit-waivers.json waives that
 *   GHSA id for that package. An expired waiver fails whether or not it still matches, so every waiver is
 *   revisited; one that matches nothing is reported for removal.
 * - Advisories are the objects in each vulnerability's `via` list (strings there only point at another
 *   vulnerable package). An unknown severity counts as critical, and a report with vulnerabilities but no
 *   readable advisory, or an npm error object, fails: the gate never passes on a shape it cannot read.
 * - The waiver file is shared with tools/ci/pip-audit.ts through `ecosystem` ("npm" when absent, or "pypi").
 */
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { repoRoot, run as realRun, type Log, type Run } from './proc.ts';

const SEVERITIES = ['info', 'low', 'moderate', 'high', 'critical'] as const;
type Severity = (typeof SEVERITIES)[number];
const rank = (s: string): number => {
  const i = SEVERITIES.indexOf(s as Severity);
  return i < 0 ? SEVERITIES.length - 1 : i;
};

export interface Advisory {
  readonly id: string;
  /** Other ids of the same advisory (pip-audit reports a PYSEC id with its GHSA and CVE aliases). */
  readonly aliases?: readonly string[];
  readonly package: string;
  readonly severity: string;
  readonly title: string;
}

export interface Waiver {
  readonly id: string;
  readonly package: string;
  readonly ecosystem: 'npm' | 'pypi';
  readonly reason: string;
  readonly expires: string;
  readonly decision: string;
}

const isRecord = (v: unknown): v is Record<string, unknown> => typeof v === 'object' && v !== null;
const str = (v: unknown, fallback: string): string => (typeof v === 'string' ? v : fallback);

export function advisoriesFrom(report: unknown): Advisory[] {
  if (!isRecord(report)) throw new Error('npm audit output is not a JSON object');
  if (isRecord(report.error)) {
    // An unreachable registry gives an empty summary and the reason in `message` [measured, npm 10.9.4].
    const reasons = [report.message, report.error.summary, report.error.detail].map((v) => str(v, ''));
    throw new Error(`npm audit failed: ${reasons.filter((r) => r !== '').join('; ') || 'no reason given'}`);
  }
  const vulnerabilities = report.vulnerabilities;
  if (!isRecord(vulnerabilities)) throw new Error('npm audit output has no vulnerabilities object');
  const found = new Map<string, Advisory>();
  for (const [name, vuln] of Object.entries(vulnerabilities)) {
    const via: unknown[] = isRecord(vuln) && Array.isArray(vuln.via) ? vuln.via : [];
    for (const v of via.filter(isRecord)) {
      const url = str(v.url, '');
      const id = /GHSA(-[a-z0-9]{4}){3}$/.exec(url)?.[0] ?? `npm-${String(v.source)}`;
      const advisory = {
        id,
        package: str(v.name, name),
        severity: str(v.severity, '?'),
        title: str(v.title, ''),
      };
      found.set(`${id} ${advisory.package}`, advisory);
    }
  }
  if (found.size === 0 && Object.keys(vulnerabilities).length > 0) {
    throw new Error('npm audit lists vulnerable packages but no advisory could be read');
  }
  return [...found.values()];
}

/** Whether a YYYY-MM-DD string names a day that exists: 2026-02-30 and 2026-99-99 do not. */
const isRealDate = (day: string): boolean => {
  const t = Date.parse(`${day}T00:00:00Z`);
  return !Number.isNaN(t) && new Date(t).toISOString().slice(0, 10) === day;
};

export function parseWaivers(json: unknown): Waiver[] {
  if (!Array.isArray(json)) throw new Error('audit-waivers.json must be an array');
  return json.map((w: unknown, i): Waiver => {
    const fields = ['id', 'package', 'reason', 'expires', 'decision'] as const;
    if (!isRecord(w) || !fields.every((f) => typeof w[f] === 'string')) {
      throw new Error(`audit-waivers.json entry ${i} needs string ${fields.join(', ')}`);
    }
    const ecosystem = w.ecosystem ?? 'npm';
    if (ecosystem !== 'npm' && ecosystem !== 'pypi')
      throw new Error(`audit-waivers.json entry ${i}: ecosystem`);
    const expires = String(w.expires);
    const real = /^\d{4}-\d{2}-\d{2}$/.test(expires) && isRealDate(expires);
    if (!/^GHSA(-[a-z0-9]{4}){3}$/.test(String(w.id)) || !real) {
      throw new Error(
        `audit-waivers.json entry ${i}: id must be a GHSA id and expires a real YYYY-MM-DD date`,
      );
    }
    return { ...(w as unknown as Waiver), ecosystem };
  });
}

/** Expired waivers of one ecosystem, as failure lines; `today` is a UTC YYYY-MM-DD date. */
export function expired(waivers: readonly Waiver[], ecosystem: Waiver['ecosystem'], today: string): string[] {
  return waivers
    .filter((w) => w.ecosystem === ecosystem && w.expires < today)
    .map((w) => `waiver ${w.id} for ${w.package} expired on ${w.expires} (${w.decision})`);
}

/** Failing, waived and unused-waiver lines for one ecosystem's advisories; a waiver matches an id or alias. */
export function evaluate(
  advisories: readonly Advisory[],
  waivers: readonly Waiver[],
  level: string,
  today: string,
  ecosystem: Waiver['ecosystem'] = 'npm',
) {
  const scoped = waivers.filter((w) => w.ecosystem === ecosystem);
  const failures = expired(scoped, ecosystem, today);
  const waived: string[] = [];
  const used = new Set<Waiver>();
  for (const a of advisories.filter((x) => rank(x.severity) >= rank(level))) {
    const line = `${a.severity} ${a.id} in ${a.package}: ${a.title}`;
    const ids = [a.id, ...(a.aliases ?? [])];
    const waiver = scoped.find((w) => ids.includes(w.id) && w.package === a.package && w.expires >= today);
    if (waiver === undefined) failures.push(line);
    else {
      used.add(waiver);
      waived.push(`${line} (waived until ${waiver.expires}, ${waiver.decision})`);
    }
  }
  const unused = scoped
    .filter((w) => !used.has(w) && w.expires >= today)
    .map((w) => `${w.id} for ${w.package}`);
  return { failures, waived, unused };
}

export function parseLevel(argv: readonly string[]): string {
  const i = argv.findIndex((a) => a === '--level' || a.startsWith('--level='));
  if (i < 0) return 'high';
  const arg = argv[i] ?? '';
  const level = arg === '--level' ? argv[i + 1] : arg.slice('--level='.length);
  if (level === undefined || !(SEVERITIES as readonly string[]).includes(level) || level === 'info') {
    throw new Error('--level must be low, moderate, high or critical');
  }
  return level;
}

export const loadWaivers = (root: string): Waiver[] =>
  parseWaivers(JSON.parse(readFileSync(join(root, 'tools', 'ci', 'audit-waivers.json'), 'utf8')));

export const today = (): string => new Date().toISOString().slice(0, 10);

export async function main(
  argv: readonly string[],
  run: Run = realRun,
  root = repoRoot,
  log: Log = console.log,
) {
  try {
    const level = parseLevel(argv);
    // npm audit exits non-zero whenever it finds anything, so its exit code carries no information here.
    const { stdout, stderr } = await run('npm', ['audit', '--json'], { cwd: root, capture: true });
    if (stdout.trim() === '') throw new Error(`npm audit printed no report: ${stderr.trim() || 'no output'}`);
    const advisories = advisoriesFrom(JSON.parse(stdout));
    const { failures, waived, unused } = evaluate(advisories, loadWaivers(root), level, today());
    for (const line of waived) log(`audit: ${line}`);
    for (const id of unused) log(`audit: waiver ${id} matches no advisory: remove it`);
    for (const line of failures) log(`audit: ${line}`);
    log(`audit: ${advisories.length} advisories, ${failures.length} failing at level ${level}`);
    return failures.length === 0 ? 0 : 1;
  } catch (error) {
    log(`audit: ${error instanceof Error ? error.message : String(error)}`);
    return 1;
  }
}

if (import.meta.main) process.exitCode = await main(process.argv.slice(2));
