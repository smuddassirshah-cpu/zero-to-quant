import { expect, it } from 'vitest';
import plugin from '../src/index.ts';

it('exports the rules of stages 1 and 3', () => {
  expect(plugin.meta.name).toBe('eslint-plugin-zq');
  expect(Object.keys(plugin.rules).sort()).toEqual([
    'layering',
    'no-colour-literals',
    'no-empty-catch',
    'no-forbidden-apis',
    'no-inner-html',
    'no-nondeterminism',
  ]);
});
