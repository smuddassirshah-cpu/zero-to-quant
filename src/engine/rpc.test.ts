// src/engine/rpc.ts against docs/ARCHITECTURE.md 5.13, in Node: the two ports of a MessageChannel stand in
// for the Worker and the worker's global scope.
import fc from 'fast-check';
import { afterEach, describe, expect, expectTypeOf, test, vi } from 'vitest';
import { connect, serve, transfer, type Endpoint, type RpcApi } from './rpc.ts';

const ports: MessagePort[] = [];
afterEach(() => {
  for (const port of ports.splice(0)) port.close();
  vi.unstubAllGlobals();
});

const BARRIER = 2 ** 40;
let barriers = BARRIER;

/** A channel whose `inbox(port)` collects what that port receives, barrier messages apart. */
function channel() {
  const { port1, port2 } = new MessageChannel();
  ports.push(port1, port2);
  const inbox = (port: MessagePort) => {
    const seen: Record<string, unknown>[] = [];
    port.addEventListener('message', (e: MessageEvent<Record<string, unknown> | null>) => {
      if (e.data && !(Number(e.data.id) > BARRIER)) seen.push(e.data);
    });
    port.start();
    return seen;
  };
  return { caller: port1, worker: port2, inbox };
}

/**
 * Resolves once the worker has handled everything `caller` posted before it, and its replies are back: a
 * port delivers in order, so the round trip of one more request is a barrier.
 */
function barrier(caller: MessagePort): Promise<void> {
  const id = ++barriers;
  return new Promise((resolve) => {
    const on = (e: MessageEvent<{ id?: unknown }>) => {
      if (e.data.id !== id) return;
      caller.removeEventListener('message', on);
      resolve();
    };
    caller.addEventListener('message', on);
    caller.postMessage({ id, m: 'barrier', a: [] });
  });
}

/** Serves `handlers` on one end and connects to the other, typed as `A`. */
function pair<A extends RpcApi>(handlers: Partial<A>) {
  const { caller, worker, inbox } = channel();
  const replies = inbox(caller);
  const requests = inbox(worker);
  serve(handlers as RpcApi, worker);
  return { client: connect<A>(caller), caller, replies, requests, settled: () => barrier(caller) };
}

function deferred() {
  let settle: (value: unknown) => void = () => undefined;
  const promise = new Promise((resolve) => {
    settle = resolve;
  });
  return {
    promise,
    resolve: (value: unknown) => {
      settle(value);
    },
  };
}

interface Api extends RpcApi {
  echo: (x: unknown, signal?: AbortSignal) => Promise<unknown>;
  add: (a: number, b: number) => Promise<number>;
  fail: (name: string, message: string) => Promise<never>;
  boom: () => Promise<never>;
  odd: (thrown: unknown) => Promise<never>;
  fn: () => Promise<() => number>;
  probe: (x: string, signal?: AbortSignal) => Promise<unknown>;
}
const api: Api = {
  echo: (x) => Promise.resolve(x),
  add: (a, b) => Promise.resolve(a + b),
  fail: (name, message) => Promise.reject(Object.assign(new Error(message), { name })),
  boom: () => {
    throw new RangeError('sync');
  },
  odd: (thrown) => {
    throw thrown;
  },
  fn: () => Promise.resolve(() => 1),
  probe: (...a) => Promise.resolve(a.map((x) => (x instanceof AbortSignal ? 'signal' : x))),
};

describe('connect and serve', () => {
  test('a Worker and a MessagePort are endpoints', () => {
    expectTypeOf<Worker>().toExtend<Endpoint>();
    expectTypeOf<MessagePort>().toExtend<Endpoint>();
  });

  test('requests carry ids counting up from 1, and each reply reaches its own call', async () => {
    const gates = [deferred(), deferred(), deferred()];
    const { client, requests, settled } = pair<{ wait: (i: number) => Promise<unknown> }>({
      wait: (i) => gates[i]?.promise ?? Promise.reject(new Error('no gate')),
    });
    const calls = [0, 1, 2].map((i) => client.call('wait', i));
    await settled();
    for (const i of [2, 0, 1]) gates[i]?.resolve(`reply ${i}`);
    expect(await Promise.all(calls)).toEqual(['reply 0', 'reply 1', 'reply 2']);
    expect(requests).toEqual([0, 1, 2].map((i) => ({ id: i + 1, m: 'wait', a: [i] })));
  });

  test("the handler gets the arguments, then its own signal in place of the caller's", async () => {
    const { client, requests, settled } = pair<Api>(api);
    const controller = new AbortController();
    expect(await client.call('probe', 'x')).toEqual(['x', 'signal']);
    expect(await client.call('probe', 'y', controller.signal)).toEqual(['y', 'signal']);
    controller.abort(); // after the call settled: no cancel is posted
    await settled();
    expect(requests.map((r) => r.a)).toEqual([['x'], ['y']]);
  });

  test("a failure rejects with the error's name and message; only those two cross", async () => {
    const { client, replies } = pair<Api>(api);
    await expect(client.call('fail', 'RangeError', 'too big')).rejects.toMatchObject({
      name: 'RangeError',
      message: 'too big',
    });
    await expect(client.call('boom')).rejects.toMatchObject({ name: 'RangeError', message: 'sync' });
    await expect(client.call('odd', 'text')).rejects.toMatchObject({ name: 'Error', message: 'text' });
    await expect(client.call('odd', 7)).rejects.toThrow('A value that is not an Error was thrown.');
    expect(replies.map((r) => Object.keys(r.e as object))).toEqual(Array(4).fill(['name', 'message']));
  });

  test('an unknown method rejects, names on the prototype chain included', async () => {
    const { client } = pair<RpcApi>(api);
    for (const m of ['missing', 'constructor', '__proto__', 'toString', 'hasOwnProperty'])
      await expect(client.call(m)).rejects.toMatchObject({
        name: 'TypeError',
        message: `No RPC method "${m}".`,
      });
  });

  test('a value postMessage cannot clone rejects the call, on either side', async () => {
    const { client, requests } = pair<Api>(api);
    await expect(client.call('echo', () => 1)).rejects.toMatchObject({ name: 'DataCloneError' });
    await expect(client.call('fn')).rejects.toMatchObject({ name: 'DataCloneError' });
    await expect(client.call('add', 2, 3)).resolves.toBe(5);
    expect(requests.map((r) => r.id)).toEqual([2, 3]);
  });

  test('transfer moves the buffers of a marked argument or result instead of copying them', async () => {
    const made = new ArrayBuffer(4);
    const { client } = pair<{
      size: (b: ArrayBuffer) => Promise<number>;
      make: () => Promise<{ b: ArrayBuffer }>;
    }>({
      size: (b) => Promise.resolve(b.byteLength),
      make: () => Promise.resolve(transfer({ b: made }, [made])),
    });
    const copied = new ArrayBuffer(8);
    const moved = new ArrayBuffer(8);
    expect(await client.call('size', copied)).toBe(8);
    expect(await client.call('size', transfer(moved, [moved]))).toBe(8);
    expect((await client.call('make')).b.byteLength).toBe(4);
    expect([copied.byteLength, moved.byteLength, made.byteLength]).toEqual([8, 0, 0]);
  });

  test("serve listens on the worker's global scope by default", async () => {
    const { caller, worker } = channel();
    vi.stubGlobal('self', worker);
    serve(api);
    await expect(connect<Api>(caller).call('add', 1, 2)).resolves.toBe(3);
  });
});

describe('cancellation and close', () => {
  test('an already aborted signal rejects at once and posts nothing', async () => {
    const { client, requests, settled } = pair<Api>(api);
    const controller = new AbortController();
    controller.abort();
    await expect(client.call('echo', 1, controller.signal)).rejects.toMatchObject({ name: 'AbortError' });
    await settled();
    expect(requests).toEqual([]);
  });

  test('aborting after the handler starts rejects at once, aborts the handler and drops its reply', async () => {
    const started = deferred();
    let inner: AbortSignal | undefined;
    const { client, replies, settled } = pair<{ hold: (signal?: AbortSignal) => Promise<unknown> }>({
      hold: (signal) => {
        inner = signal;
        started.resolve(undefined);
        return new Promise((resolve) =>
          signal?.addEventListener('abort', () => {
            resolve('late');
          }),
        );
      },
    });
    const controller = new AbortController();
    const call = client.call('hold', controller.signal);
    await started.promise;
    controller.abort();
    await expect(call).rejects.toMatchObject({ name: 'AbortError', message: 'The call was cancelled.' });
    await settled();
    expect(inner?.aborted).toBe(true);
    expect(replies).toEqual([]);
  });

  test('close rejects every pending call, cancels it in the worker, stops listening and refuses new calls', async () => {
    const gate = deferred();
    const signals: AbortSignal[] = [];
    const { client, caller, replies, settled } = pair<{ hold: (signal?: AbortSignal) => Promise<unknown> }>({
      hold: (signal) => {
        if (signal) signals.push(signal);
        return gate.promise;
      },
    });
    const calls = [client.call('hold'), client.call('hold')];
    await settled();
    const unlisten = vi.spyOn(caller, 'removeEventListener');
    client.close();
    client.close();
    expect(unlisten).toHaveBeenCalledTimes(1);
    for (const call of calls)
      await expect(call).rejects.toMatchObject({
        name: 'AbortError',
        message: 'The worker connection closed.',
      });
    await expect(client.call('hold')).rejects.toThrow('The worker connection is closed.');
    await settled(); // the cancels have reached the worker
    gate.resolve('late');
    await settled();
    expect(signals.map((s) => s.aborted)).toEqual([true, true]);
    expect(replies).toEqual([]);
  });
});

describe('malformed messages', () => {
  test('the worker ignores a message without a valid id, and fails a malformed request that has one', async () => {
    const { caller, worker, inbox } = channel();
    const replies = inbox(caller);
    serve(api, worker);
    for (const junk of [null, 'x', 3, {}, { id: 0 }, { id: -1 }, { id: 1.5 }, { id: '1' }, { id: 2 ** 53 }])
      caller.postMessage(junk);
    caller.postMessage({ id: 4, m: 3, a: [] });
    caller.postMessage({ id: 5, m: 'echo', a: 'x' });
    caller.postMessage({ id: 6, cancel: true });
    await barrier(caller);
    const failure = { ok: false, e: { name: 'TypeError', message: 'Malformed RPC request.' } };
    expect(replies).toEqual([
      { id: 4, ...failure },
      { id: 5, ...failure },
    ]);
  });

  test('the caller ignores a reply to no pending call, and fails a call whose reply is malformed', async () => {
    const { caller, worker } = channel();
    const client = connect<Api>(caller);
    const bad = [
      { ok: true },
      { ok: 'yes', r: 1 },
      { ok: false, e: { name: 1, message: 'm' } },
      { ok: false },
    ];
    const calls = bad.map(() => client.call('echo', 0));
    worker.postMessage({ id: 99, ok: true, r: 1 });
    worker.postMessage(null);
    for (const [i, reply] of bad.entries()) worker.postMessage({ id: i + 1, ...reply });
    for (const call of calls) await expect(call).rejects.toThrow('Malformed RPC reply.');
  });
});

test('every call settles, with the outcome its handler, its abort and close decide', async () => {
  type Method = 'echo' | 'fail' | 'missing' | 'hold';
  type Abort = 'none' | 'before' | 'sync' | 'started';
  type PropApi = Record<Method, (x: number, signal?: AbortSignal) => Promise<unknown>>;
  const plan = fc.record({
    method: fc.constantFrom<Method>('echo', 'fail', 'missing', 'hold'),
    abort: fc.constantFrom<Abort>('none', 'before', 'sync', 'started'),
  });
  await fc.assert(
    fc.asyncProperty(fc.array(plan, { maxLength: 12 }), fc.boolean(), async (plans, closeEarly) => {
      const started = new Map<number, () => void>();
      const handlerSignals: AbortSignal[] = [];
      const { client, replies, requests, settled } = pair<PropApi>({
        echo: (x) => Promise.resolve(x),
        fail: (x) => Promise.reject(new SyntaxError(`no ${x}`)),
        hold: (x, signal) => {
          if (signal) handlerSignals.push(signal);
          started.get(x)?.();
          return new Promise((_, reject) =>
            signal?.addEventListener('abort', () => {
              reject(new Error('stopped'));
            }),
          );
        },
      });
      const holdStarts: Promise<void>[] = [];
      const calls = plans.map(({ method, abort }, i) => {
        const controller = new AbortController();
        if (abort === 'before') controller.abort();
        if (abort === 'started' && method === 'hold')
          holdStarts.push(
            new Promise<void>((r) => started.set(i, r)).then(() => {
              controller.abort();
            }),
          );
        const call = client.call(method, i, controller.signal);
        if (abort === 'sync') controller.abort();
        return call.then(
          (value) => value,
          (e: unknown) => (e instanceof Error ? `${e.name}: ${e.message}` : 'not an Error'),
        );
      });
      if (!closeEarly)
        await Promise.all([...holdStarts, ...calls.filter((_, i) => plans[i]?.method !== 'hold')]);
      client.close();
      const cancelled = 'AbortError: The call was cancelled.';
      const expected = plans.map(({ method, abort }, i) => {
        if (abort === 'before' || abort === 'sync') return cancelled;
        if (abort === 'started' && method === 'hold' && !closeEarly) return cancelled;
        if (closeEarly || method === 'hold') return 'AbortError: The worker connection closed.';
        if (method === 'echo') return i;
        return method === 'fail' ? `SyntaxError: no ${i}` : 'TypeError: No RPC method "missing".';
      });
      expect(await Promise.all(calls)).toEqual(expected);
      await settled();
      expect(handlerSignals.every((s) => s.aborted)).toBe(true);
      const holdIds = requests.filter((r) => r.m === 'hold').map((r) => r.id);
      expect(replies.filter((r) => holdIds.includes(r.id))).toEqual([]);
    }),
    { numRuns: 60 },
  );
});
