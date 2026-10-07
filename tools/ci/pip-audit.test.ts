import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';
import type { Waiver } from './audit.ts';
import { auditArgs, exportArgs, ignored, main } from './pip-audit.ts';
import type { Run } from './proc.ts';

const waiver: Waiver = {
  id: 'GHSA-6w46-j5rx-g56g',
  package: 'pytest',
  ecosystem: 'pypi',
  reason: 'test',
  expires: '2999-01-01',
  decision: 'docs/DECISIONS.md A0',
};

const roots: string[] = [];
afterEach(() => {
  for (const dir of roots.splice(0)) rmSync(dir, { recursive: true, force: true });
});
const root = (waivers: unknown[]) => {
  const dir = mkdtempSync(join(tmpdir(), 'zq-pip-audit-test-'));
  roots.push(dir);
  mkdirSync(join(dir, 'tools', 'ci'), { recursive: true });
  writeFileSync(join(dir, 'tools', 'ci', 'audit-waivers.json'), JSON.stringify(waivers));
  return dir;
};

describe('pip-audit', () => {
  it('exports the whole lock with hashes and audits it without resolving', () => {
    expect(exportArgs('p', 'r.txt')).toEqual(
      ['export', '--project', 'p', '--locked', '--all-groups', '--no-emit-project', '--quiet'].concat([
        '--format',
        'requirements-txt',
        '--output-file',
        'r.txt',
      ]),
    );
    const audit = auditArgs('p', 'r.txt', ['GHSA-1', 'GHSA-2']);
    expect(audit.slice(0, 5)).toEqual(['run', '--project', 'p', '--locked', 'pip-audit']);
    expect(audit.slice(-8)).toEqual(
      ['--disable-pip', '--require-hashes', '-r', 'r.txt'].concat([
        '--ignore-vuln',
        'GHSA-1',
        '--ignore-vuln',
        'GHSA-2',
      ]),
    );
  });

  it('ignores only unexpired Python waivers', () => {
    const npm = { ...waiver, ecosystem: 'npm' as const };
    expect(
      ignored([waiver, npm, { ...waiver, id: 'GHSA-old', expires: '2000-01-01' }], '2026-10-07'),
    ).toEqual([waiver.id]);
  });

  it('runs export then audit, and returns the audit exit code', async () => {
    const calls: string[][] = [];
    const fake: Run = (cmd, args) => {
      calls.push([cmd, ...args]);
      return Promise.resolve({ code: calls.length === 1 ? 0 : 1, stdout: '', stderr: '', missing: false });
    };
    expect(await main(fake, root([waiver]), () => undefined)).toBe(1);
    expect(calls.map((c) => c[1])).toEqual(['export', 'run']);
    expect(calls[1]).toContain(waiver.id);
  });

  it('fails on an expired waiver, a missing uv and a failed export', async () => {
    const lines: string[] = [];
    const log = (line: string) => lines.push(line);
    const never: Run = () => Promise.reject(new Error('not called'));
    expect(await main(never, root([{ ...waiver, expires: '2000-01-01' }]), log)).toBe(1);
    expect(lines[0]).toMatch(/expired on 2000-01-01/);
    const missing: Run = () => Promise.resolve({ code: 127, stdout: '', stderr: '', missing: true });
    await expect(main(missing, root([]), log)).rejects.toThrow(/uv is not installed/);
    const failed: Run = () =>
      Promise.resolve({ code: 2, stdout: '', stderr: 'lock out of date', missing: false });
    await expect(main(failed, root([]), log)).rejects.toThrow(/uv export failed: lock out of date/);
  });
});
