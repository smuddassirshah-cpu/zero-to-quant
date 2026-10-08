// The browser project's own test (vitest.config.ts): each instance runs in the engine it is named for,
// so a misconfigured provider cannot pass three Chromium runs off as Chromium, Firefox and WebKit, and
// the workspace packages resolve through their `exports` and load as ES modules there. dmath's
// bit-identity tests run beside it in the same three engines.
import * as contracts from '@zq/contracts';
import * as mathcore from '@zq/mathcore';
import { describe, expect, it } from 'vitest';

// User-agent tokens: Chromium sends `Chrome/` (`HeadlessChrome/` when headless), Firefox `Firefox/`,
// and WebKit `AppleWebKit/` with no `Chrome/` [recalled].
function engine(agent: string): string {
  if (agent.includes('Firefox/')) return 'firefox';
  if (agent.includes('Chrome/')) return 'chromium';
  return agent.includes('AppleWebKit/') ? 'webkit' : 'unknown';
}

describe('the browser project', () => {
  it('runs each instance in the engine it names', ({ task }) => {
    const instance = /^browser \((\w+)\)$/.exec(task.file.projectName ?? '')?.[1];
    expect(instance).toMatch(/^(?:chromium|firefox|webkit)$/);
    expect(engine(navigator.userAgent)).toBe(instance);
  });

  it('imports @zq/contracts and @zq/mathcore through their exports', () => {
    expect(Object.prototype.toString.call(contracts)).toBe('[object Module]');
    expect(Object.prototype.toString.call(mathcore)).toBe('[object Module]');
  });
});
