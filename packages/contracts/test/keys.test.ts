// docs/ARCHITECTURE.md 5.5's global keys, the key column of its table as keys.ts encodes it.
import type { GlobalKey, SingleKey } from '@zq/contracts/keys';
import { describe, expectTypeOf, test } from 'vitest';
import type { Words } from './types.ts';

type Digit = Words<'1 2 3 4 5 6 7 8 9'>;

describe('the global keys (5.5)', () => {
  test('every key of the table, and no other', () => {
    expectTypeOf<GlobalKey>().toEqualTypeOf<Words<'Enter Escape H W D T ?'> | Digit>();
  });

  test('Enter and Escape are not single-character shortcuts, so the setting never turns them off', () => {
    expectTypeOf<SingleKey>().toEqualTypeOf<Words<'H W D T ?'> | Digit>();
  });
});
