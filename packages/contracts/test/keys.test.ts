// docs/ARCHITECTURE.md 5.5's global keys, as keys.ts encodes its table.
import type { GlobalAction, GlobalKey, GlobalKeymap, SingleKey } from '@zq/contracts/keys';
import { describe, expectTypeOf, test } from 'vitest';

type Digit = '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9';

describe('the global keys (5.5)', () => {
  test('one action per key in the table', () => {
    expectTypeOf<GlobalKey>().toEqualTypeOf<'Enter' | 'Escape' | 'H' | 'W' | 'D' | 'T' | Digit | '?'>();
    expectTypeOf<GlobalAction>().toEqualTypeOf<
      'primary' | 'close' | 'hints' | 'why' | 'describe' | 'table' | 'option' | 'keys'
    >();
    expectTypeOf<GlobalKeymap[Digit]>().toEqualTypeOf<'option'>();
    expectTypeOf<GlobalKeymap['?']>().toEqualTypeOf<'keys'>();
  });

  test('Enter and Escape are not single-character shortcuts, so the setting never turns them off', () => {
    expectTypeOf<SingleKey>().toEqualTypeOf<'H' | 'W' | 'D' | 'T' | Digit | '?'>();
  });
});
