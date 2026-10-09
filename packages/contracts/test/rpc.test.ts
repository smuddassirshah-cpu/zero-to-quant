// Compile-time tests of the worker RPC's wire messages (docs/ARCHITECTURE.md 5.13): `tsc -b` checks them.
import type { RpcCancel, RpcFailure, RpcReply, RpcRequest, RpcResult } from '@zq/contracts/rpc';
import { describe, expectTypeOf, test } from 'vitest';

describe('worker RPC wire messages (5.13)', () => {
  test('a request names its method and carries its arguments; a cancel names only its call', () => {
    expectTypeOf<RpcRequest>().toEqualTypeOf<{
      readonly id: number;
      readonly m: string;
      readonly a: readonly unknown[];
    }>();
    expectTypeOf<RpcCancel>().toEqualTypeOf<{ readonly id: number; readonly cancel: true }>();
    expectTypeOf<{ id: 1; cancel: false }>().not.toExtend<RpcCancel>();
  });

  test('a reply is a result or a failure, and a failure carries a name and a message, never a stack', () => {
    expectTypeOf<RpcReply>().toEqualTypeOf<RpcResult | RpcFailure>();
    expectTypeOf<RpcResult>().toEqualTypeOf<{
      readonly id: number;
      readonly ok: true;
      readonly r: unknown;
    }>();
    expectTypeOf<keyof RpcFailure['e']>().toEqualTypeOf<'name' | 'message'>();
    expectTypeOf<{ id: 1; ok: false; e: { name: 'E' } }>().not.toExtend<RpcReply>();
    expectTypeOf<{ id: 1; ok: true }>().not.toExtend<RpcReply>();
  });
});
