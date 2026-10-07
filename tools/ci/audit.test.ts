import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { describe, expect, it } from 'vitest';
import { advisoriesFrom, evaluate, expired, main, parseLevel, parseWaivers, type Waiver } from './audit.ts';
import type { Run } from './proc.ts';

// The shape of npm 10's `npm audit --json` (auditReportVersion 2), trimmed.
const report = {
  auditReportVersion: 2,
  vulnerabilities: {
    braces: {
      severity: 'high',
      via: [
        {
          source: 1240992,
          name: 'braces',
          title: 'stack exhaustion',
          url: 'https://github.com/advisories/GHSA-vfj7-8cjw-p6xm',
          severity: 'high',
        },
      ],
    },
    micromatch: { severity: 'high', via: ['braces'] },
    left: { severity: 'low', via: [{ source: 7, title: 'minor', severity: 'low', url: '' }] },
    odd: { severity: 'x', via: [{ source: 8, name: 'odd', title: 'new scale', severity: 'severe' }] },
  },
};

const waiver: Waiver = {
  id: 'GHSA-vfj7-8cjw-p6xm',
  package: 'braces',
  ecosystem: 'npm',
  reason: 'test',
  expires: '2026-11-07',
  decision: 'docs/DECISIONS.md A0',
};

describe('advisories', () => {
  it('reads advisory objects, names packages and ids, and skips package references', () => {
    expect(advisoriesFrom(report)).toEqual([
      { id: 'GHSA-vfj7-8cjw-p6xm', package: 'braces', severity: 'high', title: 'stack exhaustion' },
      { id: 'npm-7', package: 'left', severity: 'low', title: 'minor' },
      { id: 'npm-8', package: 'odd', severity: 'severe', title: 'new scale' },
    ]);
    expect(advisoriesFrom({ vulnerabilities: {} })).toEqual([]);
  });

  it.each([
    [null, /not a JSON object/],
    [{ error: { summary: 'ENOTFOUND registry' } }, /npm audit failed: ENOTFOUND/],
    [{ message: 'request failed, reason: ECONNREFUSED', error: { summary: '' } }, /failed: request failed/],
    [{ error: {} }, /npm audit failed: no reason given/],
    [{ metadata: {} }, /no vulnerabilities object/],
    [{ vulnerabilities: { a: { via: ['b'] } } }, /no advisory could be read/],
  ])('fails closed on %j', (input, message) => {
    expect(() => advisoriesFrom(input)).toThrow(message);
  });
});

describe('evaluate', () => {
  const advisories = advisoriesFrom(report);

  it('fails at or above the level, counting an unknown severity as critical', () => {
    expect(evaluate(advisories, [], 'high', '2026-10-07').failures).toEqual([
      'high GHSA-vfj7-8cjw-p6xm in braces: stack exhaustion',
      'severe npm-8 in odd: new scale',
    ]);
    expect(evaluate(advisories, [], 'low', '2026-10-07').failures).toHaveLength(3);
  });

  it('honours a waiver until it expires, then fails it', () => {
    const live = evaluate(advisories, [waiver], 'high', '2026-11-07');
    expect(live.failures).toEqual(['severe npm-8 in odd: new scale']);
    expect(live.waived[0]).toMatch(/waived until 2026-11-07/);
    const late = evaluate([], [waiver], 'high', '2026-11-08');
    expect(late.failures).toEqual([
      'waiver GHSA-vfj7-8cjw-p6xm for braces expired on 2026-11-07 (docs/DECISIONS.md A0)',
    ]);
    expect(evaluate([], [waiver], 'high', '2026-10-07').unused).toEqual(['GHSA-vfj7-8cjw-p6xm for braces']);
  });

  it('keeps ecosystems apart and matches a waiver by alias', () => {
    const pypi = { ...waiver, ecosystem: 'pypi' as const };
    expect(evaluate(advisories.slice(0, 1), [pypi], 'high', '2026-10-07').failures).toHaveLength(1);
    expect(expired([pypi, waiver], 'pypi', '2027-01-01')).toHaveLength(1);
    const aliased = {
      id: 'PYSEC-1',
      aliases: [waiver.id],
      package: 'braces',
      severity: 'unrated',
      title: '',
    };
    expect(evaluate([aliased], [pypi], 'low', '2026-10-07', 'pypi').waived).toHaveLength(1);
  });
});

describe('inputs', () => {
  it('parses --level in both spellings and rejects others', () => {
    expect(parseLevel([])).toBe('high');
    expect(parseLevel(['--level', 'moderate'])).toBe('moderate');
    expect(parseLevel(['--level=critical'])).toBe('critical');
    expect(() => parseLevel(['--level'])).toThrow(/--level must be/);
    expect(() => parseLevel(['--level=info'])).toThrow(/--level must be/);
  });

  it('validates waivers', () => {
    const bare = Object.fromEntries(Object.entries(waiver).filter(([k]) => k !== 'ecosystem'));
    expect(parseWaivers([bare])).toEqual([waiver]);
    expect(() => parseWaivers({})).toThrow(/must be an array/);
    expect(() => parseWaivers([{ id: 'x' }])).toThrow(/entry 0 needs/);
    expect(() => parseWaivers([{ ...waiver, ecosystem: 'cargo' }])).toThrow(/ecosystem/);
    for (const expires of ['soon', '2026-99-99', '2026-02-30']) {
      expect(() => parseWaivers([{ ...waiver, expires }])).toThrow(/a real YYYY-MM-DD date/);
    }
    expect(parseWaivers([{ ...waiver, expires: '2028-02-29' }])).toHaveLength(1);
  });
});

describe('main', () => {
  const root = (waivers: unknown[]) => {
    const dir = mkdtempSync(join(tmpdir(), 'zq-audit-'));
    mkdirSync(join(dir, 'tools', 'ci'), { recursive: true });
    writeFileSync(join(dir, 'tools', 'ci', 'audit-waivers.json'), JSON.stringify(waivers));
    return dir;
  };
  const npm =
    (stdout: string, stderr = ''): Run =>
    () =>
      Promise.resolve({ code: 1, stdout, stderr, missing: false });

  it('fails on unwaived advisories and passes when they are waived', async () => {
    const lines: string[] = [];
    const log = (line: string) => lines.push(line);
    const one = JSON.stringify({ vulnerabilities: { braces: report.vulnerabilities.braces } });
    const [bare, waived] = [root([]), root([{ ...waiver, expires: '2999-01-01' }])];
    try {
      expect(await main([], npm(one), bare, log)).toBe(1);
      expect(await main(['--level', 'high'], npm(one), waived, log)).toBe(0);
      expect(await main([], npm('', 'npm error audit endpoint returned an error'), bare, log)).toBe(1);
      expect(lines.at(-1)).toBe(
        'audit: npm audit printed no report: npm error audit endpoint returned an error',
      );
      expect(await main([], npm('null'), bare, log)).toBe(1);
      expect(lines.at(-1)).toBe('audit: npm audit output is not a JSON object');
    } finally {
      for (const dir of [bare, waived]) rmSync(dir, { recursive: true, force: true });
    }
  });
});
