/*
 * Typed worker RPC (docs/ARCHITECTURE.md 5.13) over the wire messages of @zq/contracts/rpc.
 * Decision notes:
 * - Ids count up from 1 per connection. An AbortSignal passed as a call's last argument stays on this side:
 *   aborting posts a cancel and rejects the call at once with an AbortError, and serve() drops the late
 *   reply. serve() passes every handler its own AbortSignal after the arguments it received, so an RPC
 *   method's only optional parameter is a trailing signal (anything else optional goes in an options
 *   object), and a caller without a signal omits it rather than passing undefined [our choice]. Rejected:
 *   the signal as `this`, which arrow-function handlers cannot read.
 * - A failure crosses as the error's name and message only, never its stack (docs/PLAN.md 8.2); the caller
 *   rejects with an Error of that name and message.
 * - Each end checks only the shape of what it receives, by hand until zod/mini is wired (docs/PLAN.md 7.2);
 *   payloads are the API's to validate. A message without a valid id is ignored, as the proxy stream ignores
 *   unknown events (7.2); a malformed message with a live id fails that call, so no caller waits forever.
 * - postMessage structured-clones, and a value it cannot clone fails the call on either side.
 *   transfer(value, list) marks a value whose buffers move instead of being copied, once.
 * - serve() looks up own properties only, so a method name such as `constructor` or `__proto__` cannot
 *   reach the prototype chain.
 */
import type { RpcCancel, RpcFailure, RpcReply, RpcRequest } from '@zq/contracts/rpc';

export type RpcApi = Record<string, (...args: never[]) => Promise<unknown>>;

/** What both ends post through: a Worker on the main thread, the worker's global scope, or a MessagePort. */
export interface Endpoint {
  postMessage(message: unknown, transfer: Transferable[]): void;
  addEventListener(type: 'message', fn: (e: MessageEvent) => void): void;
  removeEventListener(type: 'message', fn: (e: MessageEvent) => void): void;
}

const marks = new WeakMap<object, Transferable[]>();

/** Marks `value` so that the next call or reply carrying it transfers `list` instead of copying it. */
export function transfer<T extends object>(value: T, list: Transferable[]): T {
  marks.set(value, list);
  return value;
}

function transfers(values: readonly unknown[]): Transferable[] {
  return values.flatMap((value) => {
    const list = typeof value === 'object' && value !== null ? marks.get(value) : undefined;
    if (list) marks.delete(value as object);
    return list ?? [];
  });
}

const record = (v: unknown): v is Record<string, unknown> => typeof v === 'object' && v !== null;
/** A message's id, or 0 when it has none: ids start at 1, so 0 matches no call. */
const idOf = (v: unknown) =>
  record(v) && typeof v.id === 'number' && Number.isSafeInteger(v.id) && v.id > 0 ? v.id : 0;
const failure = (id: number, error: unknown): RpcFailure => ({
  id,
  ok: false,
  e:
    error instanceof Error
      ? { name: error.name, message: error.message }
      : {
          name: 'Error',
          message: typeof error === 'string' ? error : 'A value that is not an Error was thrown.',
        },
});
const aborted = (message: string) => new DOMException(message, 'AbortError');

export interface RpcClient<A extends RpcApi> {
  call<K extends keyof A & string>(m: K, ...a: Parameters<A[K]>): ReturnType<A[K]>;
  /** Rejects every pending call with an AbortError, cancels it in the worker and stops listening. */
  close(): void;
}

export function connect<A extends RpcApi>(worker: Endpoint): RpcClient<A> {
  interface Pending {
    resolve: (r: unknown) => void;
    reject: (e: unknown) => void;
    signal: AbortSignal | undefined;
    onAbort: () => void;
  }
  const pending = new Map<number, Pending>();
  let last = 0;
  let closed = false;
  const settle = (id: number) => {
    const call = pending.get(id);
    pending.delete(id);
    call?.signal?.removeEventListener('abort', call.onAbort);
    return call;
  };
  const cancel = (id: number, message: string) => {
    settle(id)?.reject(aborted(message));
    worker.postMessage({ id, cancel: true } satisfies RpcCancel, []);
  };
  const onMessage = ({ data }: MessageEvent) => {
    const call = settle(idOf(data));
    if (!call || !record(data)) return;
    const e = data.e;
    if (data.ok === true && 'r' in data) call.resolve(data.r);
    else if (data.ok === false && record(e) && typeof e.name === 'string' && typeof e.message === 'string')
      call.reject(Object.assign(new Error(e.message), { name: e.name }));
    else call.reject(new TypeError('Malformed RPC reply.'));
  };
  worker.addEventListener('message', onMessage);

  return {
    call(m, ...rest) {
      const a: readonly unknown[] = rest;
      return new Promise((resolve, reject) => {
        const tail = a.at(-1);
        const signal = tail instanceof AbortSignal ? tail : undefined;
        if (closed) throw aborted('The worker connection is closed.');
        if (signal?.aborted) throw aborted('The call was cancelled.');
        const id = ++last;
        const args: readonly unknown[] = signal ? a.slice(0, -1) : a;
        const onAbort = () => {
          cancel(id, 'The call was cancelled.');
        };
        pending.set(id, { resolve, reject, signal, onAbort });
        signal?.addEventListener('abort', onAbort, { once: true });
        try {
          worker.postMessage({ id, m, a: args } satisfies RpcRequest, transfers(args));
        } catch (error) {
          settle(id);
          throw error;
        }
      }) as never;
    },
    close() {
      if (closed) return;
      closed = true;
      worker.removeEventListener('message', onMessage);
      for (const id of [...pending.keys()]) cancel(id, 'The worker connection closed.');
    },
  };
}

/** Answers calls on `port`, the worker's own global scope unless a port is given. */
export function serve(api: RpcApi, port: Endpoint = self as unknown as Endpoint): void {
  const running = new Map<number, AbortController>();
  // False for a cancelled call, whose reply is dropped.
  const finish = (id: number, controller: AbortController) =>
    running.get(id) === controller && running.delete(id);
  const reply = (message: RpcReply, values: readonly unknown[]) => {
    try {
      port.postMessage(message, transfers(values));
    } catch (error) {
      port.postMessage(failure(message.id, error), []);
    }
  };
  port.addEventListener('message', ({ data }) => {
    const id = idOf(data);
    if (!id || !record(data)) return;
    if (data.cancel === true) {
      running.get(id)?.abort();
      running.delete(id);
      return;
    }
    const { m, a } = data;
    if (typeof m !== 'string' || !Array.isArray(a)) {
      reply(failure(id, new TypeError('Malformed RPC request.')), []);
      return;
    }
    const controller = new AbortController();
    running.set(id, controller);
    const handler: unknown = Object.hasOwn(api, m) ? api[m] : undefined;
    new Promise<unknown>((resolve) => {
      if (typeof handler !== 'function') throw new TypeError(`No RPC method "${m}".`);
      resolve(Reflect.apply(handler, api, [...(a as unknown[]), controller.signal]));
    }).then(
      (r: unknown) => {
        if (finish(id, controller)) reply({ id, ok: true, r }, [r]);
      },
      (error: unknown) => {
        if (finish(id, controller)) reply(failure(id, error), []);
      },
    );
  });
}
