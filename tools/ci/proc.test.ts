import { describe, expect, it } from 'vitest';
import { run } from './proc.ts';

describe('run', () => {
  it('captures output and the exit code', async () => {
    const script = 'process.stdout.write("out"); process.stderr.write("err"); process.exit(3)';
    expect(await run(process.execPath, ['-e', script], { capture: true })).toEqual({
      code: 3,
      stdout: 'out',
      stderr: 'err',
      missing: false,
    });
  });

  it('passes output through when not capturing', async () => {
    expect((await run(process.execPath, ['-e', 'process.exit(0)'])).code).toBe(0);
  });

  it('reports a command that is not installed', async () => {
    expect(await run('zq-no-such-command', [])).toMatchObject({ code: 127, missing: true });
  });
});
