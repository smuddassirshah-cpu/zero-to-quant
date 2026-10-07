import { afterEach, describe, expect, it } from 'vitest';
import { boot } from './boot.ts';

// A minimal element stand-in: the empty app touches only these members.
function fakeRoot() {
  const children: { textContent: string }[] = [];
  const root = {
    dataset: {} as Record<string, string>,
    replaceChildren: (...nodes: { textContent: string }[]) => children.splice(0, children.length, ...nodes),
  };
  return { root, children };
}

describe('boot', () => {
  afterEach(() => {
    Reflect.deleteProperty(globalThis, 'document');
  });

  it.each([
    ['web', false, 'The engine is being built.'],
    ['artifact', true, 'Development build, artifact platform'],
  ] as const)('renders the %s target', (target, devRoutes, line) => {
    const { root, children } = fakeRoot();
    Object.assign(globalThis, { document: { createElement: () => ({ textContent: '' }) } });
    boot(root as unknown as HTMLElement, { target, devRoutes });
    expect(children.map((c) => c.textContent)).toEqual(['Zero to Quant', line]);
    expect(root.dataset.zqBoot).toBe(target);
  });
});
