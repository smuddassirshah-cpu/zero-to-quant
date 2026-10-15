/*
 * The engine's Scope (docs/ARCHITECTURE.md 5.1, decision 13): every timer, frame, listener, effect and owned
 * disposer of one screen or widget, released together.
 * Decision notes:
 * - Each registration is an entry in its scope's live set, and its callback runs only while that entry is
 *   live, so nothing runs once it is cancelled or its scope disposed: not a callback the platform had queued,
 *   nor an event a disposer dispatches while the scope is being released [our choice].
 * - dispose() first closes the whole subtree (every descendant reads as disposed, every entry dies), then
 *   releases it. Each scope aborts its own signal as its release starts, then runs its entries in reverse
 *   order of registration, a child's subtree as one entry and an effect's entry taken before its first run.
 *   So a descendant reads as disposed before its signal aborts, which waits until its parent's release
 *   reaches it, after the parent's later registrations. A throwing disposer does not stop the rest; one
 *   error is rethrown as itself, several as an AggregateError. Registering on a disposed scope throws: it
 *   is a development error.
 * - The one module allowed raw setTimeout, setInterval and requestAnimationFrame (zq/no-raw-timers, 10.4).
 *   Frames come from a FrameSource, the browser's by default, because Node has none; timers use the
 *   globals, which vitest's fake timers replace.
 * - Insertion-ordered sets: cancel is O(1), dispose O(n) in the subtree's registrations.
 */
import { effect } from '@preact/signals-core';
import type { Scope } from '@zq/contracts/base';

/** Where animation frames come from: requestAnimationFrame in the browser, a fake clock in tests. */
export interface FrameSource {
  /** Calls fn later, never before request returns, as requestAnimationFrame does; loop() relies on it. */
  request(fn: (t: number) => void): number;
  cancel(handle: number): void;
}

type Raf = Partial<Pick<typeof globalThis, 'requestAnimationFrame' | 'cancelAnimationFrame'>>;

const browserFrames: FrameSource = {
  request(fn) {
    const host = globalThis as Raf;
    if (!host.requestAnimationFrame)
      throw new Error('No requestAnimationFrame here: pass createScope a FrameSource.');
    return host.requestAnimationFrame(fn);
  },
  cancel(handle) {
    (globalThis as Raf).cancelAnimationFrame?.(handle);
  },
};

type Entry = () => void;
type EffectFn = Parameters<typeof effect>[0];

class ScopeNode implements Scope {
  readonly #controller = new AbortController();
  readonly #live = new Set<Entry>();
  readonly #children = new Set<ScopeNode>();
  readonly #frames: FrameSource;
  #link: { parent: ScopeNode; entry: Entry } | undefined; // a child's entry in its parent
  #dying: Entry[] = [];
  #disposed = false;

  constructor(frames: FrameSource) {
    this.#frames = frames;
  }

  get signal(): AbortSignal {
    return this.#controller.signal;
  }

  get disposed(): boolean {
    return this.#disposed;
  }

  later(fn: () => void, ms: number): () => void {
    const entry = this.#add(() => {
      clearTimeout(id);
    });
    const id = setTimeout(() => {
      if (this.#live.delete(entry)) fn();
    }, ms);
    return this.#canceller(entry);
  }

  every(fn: () => void, ms: number): () => void {
    const entry = this.#add(() => {
      clearInterval(id);
    });
    const id = setInterval(() => {
      if (this.#live.has(entry)) fn();
    }, ms);
    return this.#canceller(entry);
  }

  frame(fn: (t: number) => void): () => void {
    const entry = this.#add(() => {
      this.#frames.cancel(handle);
    });
    const handle = this.#request(entry, (t) => {
      if (this.#live.delete(entry)) fn(t);
    });
    return this.#canceller(entry);
  }

  /** `dt` is 0 on the first frame, then the time since the previous one. */
  loop(fn: (t: number, dt: number) => boolean): () => void {
    let previous: number | undefined;
    const entry = this.#add(() => {
      this.#frames.cancel(handle);
    });
    const tick = (t: number) => {
      if (!this.#live.has(entry)) return;
      const dt = previous === undefined ? 0 : t - previous;
      previous = t;
      if (!fn(t, dt)) this.#live.delete(entry);
      else if (this.#live.has(entry)) handle = this.#frames.request(tick);
    };
    let handle = this.#request(entry, tick);
    return this.#canceller(entry);
  }

  listen(
    target: EventTarget,
    type: string,
    fn: (e: Event) => void,
    opts?: { capture?: boolean; once?: boolean; passive?: boolean; signal?: AbortSignal },
  ): void {
    const once = opts?.once === true;
    const entry = this.#add(() => {
      target.removeEventListener(type, handler, opts?.capture === true);
    });
    const handler = (e: Event) => {
      if (once ? this.#live.delete(entry) : this.#live.has(entry)) fn(e);
    };
    target.addEventListener(type, handler, opts);
  }

  effect(fn: EffectFn): void {
    // The entry comes before the first run, so what that run registers is released before the effect stops.
    let stop: (() => void) | undefined;
    const entry = this.#add(() => {
      stop?.();
    });
    const closed = () => this.#disposed;
    try {
      stop = effect(function (this: { dispose: () => void }) {
        return closed() ? undefined : fn.call(this);
      });
    } catch (error) {
      this.#live.delete(entry); // signals has disposed the effect; a throwing first run leaves no entry
      throw error;
    }
    // A first run that disposed this scope released the entry before `stop` existed.
    if (closed()) stop();
  }

  own(dispose: () => void): void {
    this.#add(() => {
      dispose();
    });
  }

  child(): Scope {
    const kid = new ScopeNode(this.#frames);
    const entry = this.#add(() => {
      kid.#release();
    });
    kid.#link = { parent: this, entry };
    this.#children.add(kid);
    return kid;
  }

  dispose(): void {
    if (this.#disposed) return;
    this.#close();
    if (this.#link) {
      this.#link.parent.#live.delete(this.#link.entry);
      this.#link.parent.#children.delete(this);
    }
    this.#release();
  }

  #assertLive(): void {
    if (this.#disposed) throw new Error('This scope is disposed: register on a live scope.');
  }

  #add(entry: Entry): Entry {
    this.#assertLive();
    this.#live.add(entry);
    return entry;
  }

  /** Requests a frame for a new entry, which dies with it if the source throws. */
  #request(entry: Entry, fn: (t: number) => void): number {
    try {
      return this.#frames.request(fn);
    } catch (error) {
      this.#live.delete(entry);
      throw error;
    }
  }

  #canceller(entry: Entry): () => void {
    return () => {
      if (this.#live.delete(entry)) entry();
    };
  }

  #close(): void {
    this.#disposed = true;
    this.#dying = [...this.#live].reverse();
    this.#live.clear();
    for (const kid of this.#children) kid.#close();
    this.#children.clear();
  }

  #release(): void {
    this.#controller.abort();
    const errors: unknown[] = [];
    for (const entry of this.#dying) {
      try {
        entry();
      } catch (error) {
        errors.push(error);
      }
    }
    this.#dying = [];
    if (errors.length === 1) throw errors[0];
    if (errors.length > 1) throw new AggregateError(errors, `${errors.length} disposers of a scope threw.`);
  }
}

/** A root scope. Screens and widgets take children of it (ARCHITECTURE.md 5.4, step 3). */
export function createScope(frames: FrameSource = browserFrames): Scope {
  return new ScopeNode(frames);
}
