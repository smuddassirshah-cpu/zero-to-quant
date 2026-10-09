/*
 * The worker RPC's wire messages (docs/ARCHITECTURE.md 5.13), which src/engine/rpc.ts posts and checks.
 * Decision notes:
 * - Short keys (`m`, `a`, `r`, `e`) because every call crosses postMessage; ids are positive safe integers,
 *   counted per connection.
 * - An error crosses as its name and message only, never its stack (docs/PLAN.md 8.2) [our choice].
 * - Names no DOM type, so a worker project on the WebWorker lib can import it (docs/DECISIONS.md B43).
 */

/** Caller to worker: run method `m` with arguments `a` (structured-cloned; an AbortSignal stays behind). */
export type RpcRequest = Readonly<{ id: number; m: string; a: readonly unknown[] }>;
/** Caller to worker: the call `id` was cancelled; its reply, if any, is dropped. */
export type RpcCancel = Readonly<{ id: number; cancel: true }>;
/** Worker to caller: the call `id` resolved with `r`. */
export type RpcResult = Readonly<{ id: number; ok: true; r: unknown }>;
/** Worker to caller: the call `id` failed; the caller rejects with an Error of this name and message. */
export type RpcFailure = Readonly<{ id: number; ok: false; e: Readonly<{ name: string; message: string }> }>;
export type RpcReply = RpcResult | RpcFailure;
